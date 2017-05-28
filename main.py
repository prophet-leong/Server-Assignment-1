"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)

import urllib2
import json
import random
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


Word = ""
WordProgress = list("")
bad_guesses = 0

games_won =0
games_lost = 0
@app.route('/')
def hello():
	return render_template('index.html')
	
@app.route('/new_game', methods=['POST'])
def newGame():
	#initialize
	global Word
	global WordProgress
	global bad_guesses
	
	Word = ""
	WordProgress
	bad_guesses = 0

	word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
	response = urllib2.urlopen(word_site)
	txt = response.read()
	Word = random.choice(txt.splitlines())
	#trash codes
	tempstring = ""
	for letter in range(len(Word)):
		tempstring +="_"
	WordProgress = list(tempstring)
	length = len(Word)
	return json.dumps({"word_length":length})

@app.route('/check_letter', methods = ['POST'])
def checkLetter():
	guess = str(request.json)
	character = guess[len(guess)-3]
	contains = IfLetterExist(character,Word)
	global WordProgress
	global games_won
	global games_lost
	
	if "".join(WordProgress) == Word.upper():
		games_won +=1
		return json.dumps({"game_state":"WIN","word_state":"".join(WordProgress)})
	
	if contains == False:
		global bad_guesses
		bad_guesses+= 1
		if bad_guesses >= 8: #lose
			games_lost +=1
			return json.dumps({"game_state":"LOSE","word_state":"".join(WordProgress),"answer":Word})
	
		
	return json.dumps({"game_state":"ONGOING","word_state":"".join(WordProgress),"bad_guesses":bad_guesses})


@app.route('/score', methods = ['GET'])
def GetScore():
	return json.dumps({"games_won":games_won,"games_lost":games_lost})

@app.route('/score', methods = ['DELETE'])
def DeleteScore():
	global games_won
	games_won = 0
	global games_lost
	games_lost = 0
	
	return json.dumps({"games_won":games_won,"games_lost":games_lost})
	
	
def IfLetterExist(character , word):
	count = 0
	contains = False
	for letter in range(len(Word)):
		if Word[count] == character.lower():
			contains = True
			global WordProgress
			WordProgress[count] = character
			
		count+=1
		print(WordProgress)
	return contains
		
	
	

	
		


	
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
