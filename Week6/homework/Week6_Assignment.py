import time, logging
from flask import Flask, render_template
from gqlalchemy import Memgraph


log = logging.getLogger(__name__)

app = Flask(__name__)

memgraph = Memgraph()
connection_established = False
# while (not connection_established):
# 	try:
# 		if (memgraph._get_cached_connection().is_active()):
# 			connection_established = True
# 	except:
# 		time.sleep(4)

def index():
	return "Hi World"

@app.route('/')
def generate_data():
	# memgraph.drop_database()
	#_ This is to populate database
	#_ For dropping everything we have in memgraph
	#_ Because we will be constantly restarting app
	#_ And would just be adding on new data
	#_ Instead, want to refresh data.
	return "0"

def main():
	# generate_data()
	# index()
	app.run()

if (__name__ == "__main__"):
	# app.run(host="0.0.0.0", debug=True)
	main()