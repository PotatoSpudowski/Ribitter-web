from flask import Flask, redirect, session,render_template
from flask import request
import flask 
import tweepy
from requests_oauthlib import OAuth1Session
import requests
import json
from configparser import ConfigParser

app = Flask(__name__)

#config
	
config_object = ConfigParser()
config_object.read("config.ini")

config_object = config_object["CONFIG"]
consumer_key = config_object["consumer_key"]
consumer_secret = config_object["consumer_secret"]
callback = config_object["callback"]


elixrApi = config_object["elixrApi"]
mismatchApi = config_object["mismatchApi"]


@app.route('/auth')
def auth():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
	url = auth.get_authorization_url()
	session['request_token'] = auth.request_token
	return redirect(url)

@app.route('/callback')
def twitter_callback():
	request_token = session['request_token']
	del session['request_token']

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
	auth.request_token = request_token
	verifier = request.args.get('oauth_verifier')
	auth.get_access_token(verifier)
	session['token'] = (auth.access_token, auth.access_token_secret)

	return redirect('/me')

user_Dict={}

@app.route('/me')
def request_user_data():
	global user_Dict
	token, token_secret = session['token']
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
	auth.set_access_token(token, token_secret)
	api = tweepy.API(auth)

	userData = api.me()._json
	user_Dict={
			"id":userData['id'],
			"screen_name":userData['screen_name'],
			"name":userData['name'],
			"description":userData['description'],
			"location":userData['location'],
			"entities":userData['entities'],
			"profile_image_url":userData['profile_image_url']
	}
	return redirect('/home-timeline')

textLabel=[]
tweetsIds=[]
hideId=[]

@app.route('/home-timeline')
def request_timeline():
	global textLabel
	global tweetsIds
	global hideId
	token, token_secret = session['token']
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
	auth.set_access_token(token, token_secret)
	api = tweepy.API(auth)

	timeline = api.home_timeline(tweet_mode="extended")

	timeline_data = []
	textLabel=[]
	for td in timeline:
		td = td._json
		_id = td['id']
		lang = td['lang']
		place = td['place']
		text = td['full_text']
		geo = td['geo']
		user = {
			"id": td['user']['id'],
			"name": td['user']['name'],
			"screen_name": td['user']['screen_name'],
			"profile_url": td['user']['profile_image_url']
		}
		entities = td['entities']

		if "extended_entities" in td:
			extended_entities = td['extended_entities']
		else:
			extended_entities = {}

		if _id not in hideId:
			timeline_data.append({
				"id":_id,
				"text":text,
				"lang":lang,
				"geo":geo,
				"place":place,
				"user":user,
				"entities":entities,
				"extended_entities":extended_entities
			})
		textLabel.append(text)
		tweetsIds.append(_id)

	return render_template('tweets.html', data=timeline_data, user=user_Dict, txt=txt)

@app.route('/labels', methods = ['POST'])
def getLabel():
	global hideId
	labels1 = request.form['array[]']
	labels=labels1.split(',')
	url = '{}/predict'.format(elixrApi)
	myobj = {'sentences': textLabel,"ids":tweetsIds,'labels': labels}
	y=json.dumps(myobj)
	y=json.loads(y)
	x = requests.post(url, json = y)
	resObj=json.loads(x.text)
	filterData=resObj['data']
	hideId=[]
	for z in filterData:
		for y in z['predictions']:
			if (z['predictions'][y])>0.7:
				hideId.append(z['tweet_id'])
	return redirect('/home-timeline')

txt=""

@app.route('/misinfo', methods = ['POST'])
def getInfo():
	global txt
	tweetTxt = request.form['text'].split(',')
	txt=tweetTxt[0]
	tweetId=tweetTxt[1]
	url = '{}/predict'.format(mismatchApi)
	myobj = {'sentence': txt,'id':tweetId}
	y=json.dumps(myobj)
	y=json.loads(y)
	x = requests.post(url, json = y)
	resObj=json.loads(x.text)
	filterData=resObj['data']
	txt=filterData['class']
	return redirect('/home-timeline')

@app.route('/direct-message')
def request_dm():
	token, token_secret = session['token']
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
	auth.set_access_token(token, token_secret)
	api = tweepy.API(auth)

	dm_object = api.list_direct_messages(count=1000)

	dm_list = [dm_data._json for dm_data in dm_object]

	return {
		"status":200,
		"data":dm_list
	}

# @app.route('/delete-direct-message')
# def delete_dm():
# 	token, token_secret = session['token']
# 	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
# 	auth.set_access_token(token, token_secret)
# 	api = tweepy.API(auth)

# 	dm_object = api.destroy_direct_message(1328940318226591749)

# 	return {
# 		"status":200,
# 	}

if __name__ == "__main__":
	app.secret_key = 'GimmeAJob'
	app.run()