import nltk
from nltk.corpus import words as w
import json
from flask import Flask, render_template,request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dc883876a3212fab8015ed91f26d8440071ff400c0a0dcd4'

guessList=[]


def read_file():
    file = open('word.json')
    words = json.load(file)
    file.close()
    #print(word)
    return words

def get_wordList():
    wordList = read_file()
    return wordList

def get_word(word_id,wordList):
    word = wordList[word_id-1]
    if word is None:
        abort(404)
    return word


def check_valid_word(wordToCheck):
    wordToCheck=wordToCheck.lower()
    return wordToCheck in w.words()
     

#Check only 1 letter changed    
def compare_strings(wordToCheck,wordToCompare):
    count=0;
    for (x, y) in zip(wordToCheck, wordToCompare):
        if x != y:
            count+=1
    return count 


def reset_guessList():
    return guessList.clear()

@app.route('/',defaults={'word_id': 1}, methods=('GET', 'POST'))
@app.route('/<int:word_id>', methods = ('GET', 'POST'))
def index(word_id):
    wordList=get_wordList()
    print(len(wordList))
    print("outside if word_id",word_id)
    if word_id == 0:
        word_id = len(wordList)
        print("inside if word_id",word_id)
        return redirect(url_for('index',word_id=word_id))
    elif word_id > len(wordList):
        word_id = 1
        print("word_id",word_id)
        return redirect(url_for('index',word_id=word_id))
    count=0
    word = get_word(word_id,wordList)
    if request.method == 'GET':
        reset_guessList()
    if request.method == 'POST':
        guessed = request.form['word']
        if not guessed:
            flash('Enter a word')
        elif len(guessed) < 4:
            flash('Enter a 4 letter word')
        else:
            if check_valid_word(guessed):
                if(len(guessList)>0):
                    if guessed == guessList[-1]:
                        flash('Enter a different word')
                    else:
                        count = compare_strings(guessed,guessList[-1])
                else:
                   count = compare_strings(guessed,word['from'])
                if count ==1:
                    if compare_strings(guessed,word['to']) ==1:
                        flash('You did it!')
                    guessList.append(guessed)
                else:
                    flash('Please change 1 letter')
            else:
                flash('This is not a valid word')
    return render_template('index.html', word=word, guessList=guessList)

