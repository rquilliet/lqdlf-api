# mongo.py

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import pprint
import certifi

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'lqdlf'
app.config['MONGO_URI'] = 'mongodb+srv://remi:Asmasm1986$@atlascluster.3befly2.mongodb.net/lqdlf?retryWrites=true&w=majority&tlsCAFile='+certifi.where()
mongo = PyMongo(app)
#APP_URL="http://localhost:5000"

@app.route('/')
def index():
  return "<h1>Les Quizz de le Foot</h1>"

@app.route('/career/<player_name>', methods=['GET'])
def get_career_by_name(player_name):
	player = mongo.db.players
	pl=player.find_one({'name':player_name})
	if pl:
		try:
			output={
			'name':pl['name'],
			'career':pl['career'],
			'height':pl['height'],
			'nationality':pl['nationality'],
			'pageviews':pl['pageviews'],
			'pop_rank':pl['pop_rank'],
			'level':pl['level']}
		except:
			output="Issue in DB with "+str(player_name)
	else:
		output="No player named "+str(player_name)
	return jsonify({'result':output})


@app.route('/career_level/<level>', methods=['GET'])
def get_career_by_level(level):
	player = mongo.db.players
	pl=player.aggregate([{'$match':{'level':level}},{'$sample':{'size':1}}])
	try:
		for p in pl:
			output={
			'name':p['name'],
			'career':p['career'],
			'height':p['height'],
			'nationality':p['nationality'],
			'pageviews':p['pageviews'],
			'pop_rank':p['pop_rank'],
			'level':p['level']}
	except:
		output="Issue in DB"
		pprint.pprint(list(pl))
	return jsonify({'result':output})

@app.route('/names/<level>', methods=['GET'])
def get_names_by_level(level):
	player = mongo.db.players
	pl=player.find({'level':level})
	output=[]
	try:
		for p in pl:
			name=p['name']
			match len(name.split(" ")):
				case 1:
					name=name
				case 2:
					name=name.split(" ")[1]
				case _:
					name=" ".join(name.split(" ")[1:])
			output.append(name)
	except:
		output="Issue in DB"
		pprint.pprint(list(pl))
	output=[*set(output)]
	output.sort()
	return jsonify({'result':output})

@app.route('/name/<level>', methods=['GET'])
def get_name_by_level(level):
	player = mongo.db.players
	pl=player.aggregate([{'$match':{'level':level}},{'$sample':{'size':1}}])
	try:
		for p in pl:
			name=p['name']
			match len(name.split(" ")):
				case 1:
					name=name
				case 2:
					name=name.split(" ")[1]
				case _:
					name=" ".join(name.split(" ")[1:])
		output=name
	except:
		output="Issue in DB"
		pprint.pprint(list(pl))
	return jsonify({'result':output})

@app.route('/players', methods=['GET']) #not finished
def get_players():
	player = mongo.db.players
	teams = request.args.get('teams', None)
	statement={}
	conditions=[]
	if teams!=None:
		for team in teams.split(","):
			condition={}
			condition['career.clubs']={}
			condition['career.clubs']['$regex']=".*"+team+".*"
			conditions.append(condition)
		
	statement['$and']=conditions
	
	output=[]
	for pl in player.find(statement):
		output.append({'name':pl['name']})

	return jsonify({'result':output})

# @app.route('/test', methods=['GET'])
# def get_test():
# 	#player = mongo.db.players
# 	teams = request.args
# 	print(teams)
# 	# statement={}
# 	# conditions=[]
# 	# if teams!=None:
# 	# 	for team in teams.split(","):
# 	# 		condition={}
# 	# 		condition['career.clubs']={}
# 	# 		condition['career.clubs']['$regex']=".*"+team+".*"
# 	# 		conditions.append(condition)
		
# 	# statement['$and']=conditions
	
# 	# output=[]
# 	# for pl in player.find(statement):
# 	# 	output.append({'name':pl['name']})
# 	#pl=player.find_one({'name':player_name})
# 	#if pl:
# 	#	output={'name' : pl['name'], 'career': pl['career']}
# 	#else:
# 	#	output="No player named " +str(player_name)
# 	return jsonify({'result':teams})


# @app.route('/star/', methods=['GET'])
# def get_one_star(name):
#   star = mongo.db.stars
#   s = star.find_one({'name' : name})
#   if s:
#     output = {'name' : s['name'], 'distance' : s['distance']}
#   else:
#     output = "No such name"
#   return jsonify({'result' : output})

# @app.route('/star', methods=['POST'])
# def add_star():
#   star = mongo.db.stars
#   name = request.json['name']
#   distance = request.json['distance']
#   star_id = star.insert({'name': name, 'distance': distance})
#   new_star = star.find_one({'_id': star_id })
#   output = {'name' : new_star['name'], 'distance' : new_star['distance']}
#   return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)
