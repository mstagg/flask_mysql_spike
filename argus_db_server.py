#!flask/bin/python
from flask import Flask
from flask.ext.cors import CORS
import MySQLdb
import datetime

app = Flask(__name__)
cors = CORS(app)
db = MySQLdb.connect(host="localhost",  		# your host 
                     user="root",       		# username
                     passwd="Banshee8396",     	# password
                     db="argus")   				# name of the database

# Creates a new session to store truck positions
@app.route('/create/session', methods=['GET'])
def new_session():
	try:
		cursor = db.cursor()
		now = datetime.datetime.now()
		time = now.isoformat()
		cursor.execute("INSERT INTO sessions(session_key, date) Values (NULL, '" + time + "')")
		db.commit()
		cursor.close()
		return "1"
	except:
		return "0"

# Logs relevant information regarding a trucks current position 
@app.route('/log/position/<string:id>/<string:tick>/<string:status>/<string:xpos>/<string:ypos>/<string:zpos>', methods=['GET'])
def log_pos(id, tick, status, xpos, ypos, zpos):
	try:
		cursor = db.cursor()
		now = datetime.datetime.now()
		time = now.isoformat()
		cursor.execute("INSERT INTO positions(session_key, id, tick, status, xpos, ypos, zpos, log_datetime) Values (last_insert_id(), '" + id + "', " + tick + ", " + status + ", " + xpos + ", " + ypos + ", " + zpos + ", '" + time + "')")
		db.commit()
		cursor.close()
		return "1"
	except:
		return "0"

# Returns a CSV formatted list of all logged truck positions for a given session ID and truck ID 
@app.route('/retrieve/positions/<string:session_key>/<string:t_id>', methods=['GET'])
def get_pos(session_key, t_id):
	try:
		cursor = db.cursor()
		cursor.execute("SELECT tick, xpos, zpos, status FROM positions WHERE session_key = " + session_key + " AND id = '" + t_id + "' ORDER BY log_datetime ASC")
		result = cursor.fetchall()
		s = ""
		for row in result:
			s += str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "<br>"
		if(len(s) > 0):
			cursor.close()
			s = s[0:len(s) - 4] # Remove last '<br>' from string 
			return s
		else:
			cursor.close()
			return "0";
	except:
		return "0"

# Returns the total length of time that a session ran for
@app.route('/retrieve/length/time/<string:session_key>', methods=['GET'])
def get_len_time(session_key):
	try:
		cursor = db.cursor()
		cursor.execute("SELECT log_datetime FROM positions WHERE session_key = " + session_key + " ORDER BY log_datetime ASC LIMIT 1")
		dateBegin = cursor.fetchone()[0]
		cursor.execute("SELECT log_datetime FROM positions WHERE session_key = " + session_key + " ORDER BY log_datetime DESC LIMIT 1")
		dateEnd = cursor.fetchone()[0]
		len = str(dateEnd - dateBegin)
		cursor.close()
		return len
	except:
		return "0"

# Returns the total amount of ticks for a specific session
@app.route('/retrieve/length/tick/<string:session_key>', methods=['GET'])
def get_len_tick(session_key):
	try:
		cursor = db.cursor()
		cursor.execute("SELECT tick FROM positions WHERE session_key = " + session_key + " ORDER BY tick DESC LIMIT 1")
		result = cursor.fetchone()[0]
		return str(result)
	except:
		return "0"

if __name__ == '__main__':
	app.run(debug = True)