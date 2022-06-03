import time, logging, random, json
#? RESEARCH LOGGING
from argparse import ArgumentParser
#? WTH IS THIS??
from enum import Enum
#? revise on wtf enum is
from flask import (
	Flask, 
	render_template,
	Response
)
from functools import wraps
#? RESEARCH WRAPS
from gqlalchemy import Memgraph, Match

log = logging.getLogger(__name__)

def initialiseLog():
	logging.basicConfig(level=logging.DEBUG)
	log.info("Logging enabled")
	logging.getLogger("werkzeug").setLevel(logging.WARNING)

initialiseLog()

def ParseArgs():
	'''
	Parse command line arguments
	'''

	parser = ArgumentParser(description=__doc__)
	parser.add_argument(
		"--app-host", 
		default="0.0.0.0",
		help="Allowed host addresses."
	)
	parser.add_argument(
		"--app-port",
		default=5000,
		type=int,
		help="App port."
	)
	parser.add_argument(
		"--template-folder",
		default="public/templates",
		help="The folder with flask templates."
	)
	parser.add_argument(
		"--static-folder",
		default="public",
		help="The folder with flask static files."
	)
	parser.add_argument(
		"--debug",
		default=True,
		action="store_true",
		help="Run web server in debug mode"
	)
	parser.add_argument(
		"--clean-on-start", 
		action="store_true",
		help="Should the DB be emptied on script start"
	)

	return parser.parse_known_args()

args, unknown = ParseArgs()

def logTime(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		start_time = time.time()
		result = func(*args, **kwargs)
		duration = time.time() - start_time
		log.info("Time for {} is {}".format(func.__name__, duration))

		return result

	return wrapper

app = Flask(
	import_name=__name__,
	template_folder=args.template_folder,
	static_folder=args.static_folder,
	static_url_path="",
)
memgraph = Memgraph()
connection_established = False

while (not connection_established):
	try:
		if (memgraph._get_cached_connection().is_active()):
			connection_established = True
	except:
		log.info("Memgraph may not be running")
		time.sleep(4)

@logTime
def InitializeData(card_count, pos_count):
	#_ CREATE CARDS
	memgraph.execute(
		"UNWIND range(0, {} - 1) AS id "
		"CREATE (:Card {{id: id, compromised: false}})".format(card_count) #* runs for every number in range
	)
	#* range of ids from 0 to card count - 1, so all nodes will have unique ID

	#_ 
	memgraph.execute(
		"UNWIND range({}, {} - 1) AS id " #* starts at IDs from card count & goes until card + pos count
		"CREATE (:Pos {{id: id, compromised: false}})".format(card_count, card_count + pos_count) #* will give us IDs after IDs of cards therefore giving sequential IDs
	)

def CompromisePOS(pos_id):
	'''
		Compromises a single POS
	'''
	memgraph.execute("MATCH (p:Pos {{id: {}}}) SET p.compromised = true".format(pos_id)) #* match a type of pos (a p node), and match by id, then compromise
	log.info("Point of sale %d is compromised" % pos_id)

@logTime
def CompromisePOSDevices(card_count, pos_count, fraud_count):
	log.info("Compromising {} out of {} POS devices".format(fraud_count, pos_count))

	compromised_devices = random.sample(range(card_count, card_count + pos_count), fraud_count)

	for p_id in compromised_devices:
		CompromisePOS(p_id)

@logTime
def PumpTransactions(card_count, pos_count, tx_count, report_pct):
	'''
		Pump Transactions into Graph
	'''

	log.info(f"Creating {tx_count} transactions")

	query = (
		"MATCH (c:Card {{id: {}}}), (p:Pos {{id: {}}}) " #* match cards & pos devices by random ids
		"CREATE (t:Transaction "
		"{{id: {}, fraudReported: c.compromised AND (rand() < %f)}}) "
		"CREATE (c)<-[:Using]-(t)-[:At]->(p) " #* create 2 transactions, one at card, and other at pos device
		"SET c.compromised = p.compromised" % report_pct #* set float variable to report_pct
	)

	#_ HELPER FUNC FOR RANDOM INTS
	def rint(min, max): return random.randint(min, max - 1)

	for i in range(card_count + pos_count, card_count + pos_count + tx_count): #* i.e., for the range of all tansactions
		memgraph.execute(query.format(rint(0, card_count), rint(card_count, card_count + pos_count), i))

@logTime
def GenerateData():
	memgraph.drop_database()
	#* will be constantly restarting app, so don't want to be continuously adding on data, but want to start with fresh data
	log.info("Generating Database...")
	#* Then populate database

	number_of_pos = 10
	number_of_cards = 20
	number_of_transactions = 30
	number_of_compromised_pos = 2
	rate_of_fraudulent_transactions = 0.1

	InitializeData(number_of_cards, number_of_pos)

	CompromisePOSDevices(number_of_cards, number_of_pos, number_of_compromised_pos)

	PumpTransactions(number_of_cards, number_of_pos, number_of_transactions, rate_of_fraudulent_transactions)

class Properties(Enum):
	#? wth is this, and what is it for?
	ID = 'id'
	FRAUDREPORTED = 'fraudReported'
	COMPROMISED = 'compromised'

@logTime
@app.route("/get-graph", methods=["GET"])
def get_graph():
	log.info("Client fetching POS connected components")
	ex = memgraph.execute_and_fetch(
		"MATCH (pos:Pos)<-[:At]-(transaction:Transaction {fraudReported: false}) "
		"RETURN pos, transaction"
	)

	# print(list(ex))

	try:
		print("here")
		# results = (Match().node("Pos", variable="pos").to("At").node("Transaction", variable="transaction").execute())
        
		print("here")

		node_set = set()
		link_set = set()
		# print(results)
		for result in ex:
			# print(result["pos"].id)
			pos_id = result["pos"].id
			pos_label = "POS " + str(pos_id)
			pos_compromised = result["pos"].compromised

			transaction_id = result["transaction"].id
			transaction_label = "Transaction" + str(transaction_id)
			transaction_fradulent = result["transaction"].fraudReported

			node_set.add((pos_id, pos_label, pos_compromised))
			node_set.add((transaction_id, transaction_label, transaction_fradulent))

			if ((pos_id, transaction_id) not in link_set and (transaction_id, pos_id) not in link_set):
				link_set.add((transaction_id, pos_id))
		
		nodes = [
			{
				"id": node_id,
				"label": node_label,
				"fraud": node_fraud
			}
			for node_id, node_label, node_fraud in node_set
		]

		links = [
			{
				"source": n_id,
				"target": m_id
			}
			for n_id, m_id in link_set
		]

		response = {
			"nodes": nodes, 
			"links": links
		}

		return Response(json.dumps(response), status=200, mimetype="application/json")
	
	except Exception as e:
		log.info("Data fetching went wrong.")
		log.info(e)
		return ("", 500)

@app.route("/", methods=["GET"])
#* This decorator makes this function the default index rount
#? Look this up further
def index():
	return render_template("index.html")

def main():
	GenerateData()
	app.run(host=args.app_host, port=args.app_port, debug=args.debug)

print(__name__)

if (__name__ == 'app'):
	main()