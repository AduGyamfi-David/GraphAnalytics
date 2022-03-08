import time, logging
from flask import Flask
from functools import wraps
from gqlalchemy import Memgraph

# log = logging.getLogger(__name__)

# def initialiseLog():
# 	logging.basicConfig(level=logging.DEBUG)
# 	log.info("Logging enabled")
# 	logging.getLogger("logger1").setLevel(logging.WARNING)

# initialiseLog()

# def logTime(func):
# 	@wraps(func)
# 	def wrapper(*args, **kwargs):
# 		start_time = time.time()
# 		result = func(*args, **kwargs)
# 		duration = time.time() - start_time
# 		log.info("Time for {} is {}".format(func.__name__, duration))

# 		return result

# 	return wrapper


app = Flask(__name__)
# memgraph = Memgraph()
# connection_established = False

# while (not connection_established):
# 	try:
# 		if (memgraph._get_cached_connection.is_active()):
# 			connection_established = True
# 	except:
# 		log.info("Memgraph may not be running")
# 		time.sleep(4)

@app.route("/")
def HelloWorld():
	return "Hello, World!"

# @log_time
# def GenerateData():
# 	memgraph.drop_database()
# 	log.info("Generating Database...")
# 	#* Then populate database

# def main():
# 	GenerateData()
# 	app.run()

# if (__name__ == '__main__'):
# 	app.run()
