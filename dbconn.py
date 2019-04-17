''' dbconn.py a basic survey engine
    Copyright (C) 2019 Bradley Sanders

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import MySQLdb, pandas
from uuid import UUID
import credentials
'''
Very simple database connector. 
'''
def connect(_db):
	try:
		return MySQLdb.connect(host='localhost',user='survey',passwd=credentials.surveyserver_password,db=_db)
	except:
		raise Exception('Unable to connect to database server -- aborting')


def save_response(userid,lastq,scale,weight):
	lastq = str(lastq).rjust(6).strip()
	userid = UUID(userid, version=4)
	vals = (userid,str(lastq),str(scale),str(weight))
	mysqlsel = "insert into responses(userid,question_number, scale, weight) values (%s, %s, %s, %s);"
	db = connect('survey')
	cursor = db.cursor()
	cursor.execute(mysqlsel,vals)
	db.commit()
	db.close()

def fetch_queries():
	mysqlsel = "select text,number from survey.questions where active='t' order by number;"
	db = connect('survey')
	cursor = db.cursor()
	cursor.execute(mysqlsel)
	df = pandas.DataFrame(list(cursor.fetchall()))
	db.close()
	df.columns = ['text','number']
	return df

def get_results(userid):
	userid = UUID(userid, version=4)
	mysqlsel = f'''select
	responses.question_number,
	responses.scale,
	responses.weight,
	responses.sent,
	questions.category,
	questions.positivemask,
	questions.text
	FROM survey.responses inner join survey.questions
	on questions.number = responses.question_number where responses.userid like \'{userid}\';'''
	db = connect('survey')
	cursor = db.cursor()
	cursor.execute(mysqlsel)
	df = pandas.DataFrame(list(cursor.fetchall()))
	df.columns = ['number','scale','weight','sent','category','positivemask','text']
	db.close()
	return df
	
