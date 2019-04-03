import os, uuid, collections, pandas, mydbconn, myresults
from bottle import route, run, template, response, request

class next_statement:
	def __init__(self,statements,thisline):
		
		try:
			line = statements.loc[statements['number'] > thisline].head(1)
			self.question = line.text.item()
			self.qnum = line.number.item()
		except:
			line = statements.loc[statements['number'] >= 1].head(1)
			self.question = line.text.item()
			self.qnum = line.number.item()
			print('line not in set ' + str(thisline))

#Get a working cursor

db = mydbconn.connect('survey')
cursor = db.cursor()

#Load the statement list into memory

statements = mydbconn.fetch_queries(cursor)
lastrow = int(statements.tail(1).number.item())
#print(statements)

@route('/')
def index():
	if request.get_cookie("account"):
		userid = request.get_cookie("account")
	else:
		response.set_cookie("account", str(uuid.uuid4()))

	return template('survey_intro')

@route('/schema')
def schema():
	if request.get_cookie("account"):
		userid = request.get_cookie("account")
	else:
		userid = str(uuid.uuid4())
		response.set_cookie("account", userid)

	if request.get_cookie("lastline"):
		lastline = int(request.get_cookie("lastline"))
	else:
		lastline = int(0)

	s = next_statement(statements,lastline)
	response.set_cookie("lastline", str(s.qnum))

	return template('response_html',n=s.qnum, q=s.question)

@route('/schema', method='POST')
def schema_post():
	scale = 1
	weight = 1
	if request.get_cookie("account"):
		userid = request.get_cookie("account")
		
		#Figure out last question answered
		try:
			lastline = int(request.params.get("q"))
			scale = int(request.params.get("s"))
			weight = int(request.params.get("w"))
		except:
			if request.get_cookie("lastline"):
				lastline = int(request.get_cookie("lastline"))
			else:
				lastline = 0

		#save result of query
		mydbconn.save_response(cursor,userid,lastline,scale,weight)

		#return next statement
		if lastline == lastrow:
			#Redirect to completion summary
			pass
		else:
			s = next_statement(statements,lastline)
			response.set_cookie("lastline", str(s.qnum))
			return template('response_html',n=s.qnum, q=s.question)

	else:
		response.set_cookie("account", str(uuid.uuid4()))
		return template('survey_intro')


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8088))
	run(host='0.0.0.0', port=port, debug=False)
