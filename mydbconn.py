import MySQLdb, pandas
'''
Very simple database connector. 
'''
def connect(_db):
	try:
		return MySQLdb.connect(host='localhost',user='survey',passwd='PASSWORD',db=_db)
	except:
		raise Exception('Unable to connect to database server -- aborting')


def save_response(cursor,userid,lastq,scale,weight):
	mysqlsel = "insert into responses(userid,question_number, scale, weight) values ('" + userid + "'," + str(lastq) + "," + str(scale) + "," + str(weight) + ");"
	try:
		cursor.execute(mysqlsel)
		db.commit()
	except:
		db = connect('survey')
		cursor = db.cursor()
		cursor.execute(mysqlsel)
		db.commit()

def fetch_queries(cursor):
	mysqlsel = "select text,number from survey.questions where active='t' order by number;"
	cursor.execute(mysqlsel)
	df = pandas.DataFrame(list(cursor.fetchall()))
	df.columns = ['text','number']
	return df

def get_results(userid):
	mysqlsel = '''select responses.userid,
	responses.question_number,
	responses.scale,
	responses.weight,
	questions.category,
	questions.domain
	FROM survey.responses inner join survey.questions
	on questions.number = responses.question_number;'''
	cursor.execute(mysqlsel)
	df = pandas.DataFrame(list(cursor.fetchall()))
	df.columns = ['userid','number','scale','weight','category','domain']
	return df
	
