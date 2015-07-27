#!flask/bin/python
from flask import Flask
from flask.ext.cors import CORS
import MySQLdb
import datetime

app = Flask(__name__)
cors = CORS(app)
db = MySQLdb.connect(host="localhost",  # your host 
                     user="root",       # username
                     passwd="Banshee8396",     # password
                     db="argus")   # name of the database
#MySQLdb.cursors.DictCursor
cursor = db.cursor()

@app.route('/create/session', methods=['GET'])
def new_session():
	try:
		now = datetime.datetime.now()
		time = now.isoformat()
		cursor.execute("INSERT INTO sessions(session_key, date) Values (NULL, '" + time + "')")
		db.commit()
		return "1"
	except:
		return "0"

@app.route('/log/position/<string:id>/<string:xpos>/<string:ypos>/<string:zpos>', methods=['GET'])
def log_pos(id, xpos, ypos, zpos):
	try:
		now = datetime.datetime.now()
		time = now.isoformat()
		cursor.execute("INSERT INTO positions(session_key, id, xpos, ypos, zpos, log_datetime) Values (last_insert_id(), '" + id + "', " + xpos + ", " + ypos + ", " + zpos + ", '" + time + "')")
		db.commit()
		return "1"
	except:
		return "0"

@app.route('/retrieve/positions/<string:session_key>', methods=['GET'])
def get_pos(session_key):
	try:
		cursor.execute("SELECT * FROM positions WHERE session_key = " + session_key + " ORDER BY log_datetime ASC")
		result = cursor.fetchall()
		s = ""
		for row in result:
			s += str(row[0]) + "," + str(row[1]) + "," + str(row[3]) + "," + str(row[5]) + "<br/>"
		if(len(s) > 0):
			return s
		else:
			return "0";
	except:
		return "0"

if __name__ == '__main__':
	app.run(debug = True)