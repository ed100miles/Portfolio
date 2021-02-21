from datetime import datetime
from flask import Flask, render_template, request, redirect
from  Scrabbler import initialise_board, wordFinder, wordScorer, wordRanker, play_move
from flask_sqlalchemy import SQLAlchemy
from tqdm import tqdm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/flaskFourTest.db'
db = SQLAlchemy(app)

class Scrabble(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(50), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    played_word = db.Column(db.String(20), nullable=False)
    direction = db.Column(db.String(1), nullable=False)
    xcoord = db.Column(db.Integer, nullable=False)
    ycoord = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.id

class Definitions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wordsToDefine = db.Column(db.String(50), nullable=False)
    wordDefinition = db.Column(db.String(20), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id

#### Used to populate database with words + definitions - takes a long time to run ####

    # wordsList = list((open("/home/ed/Documents/VSCode/scrabbler/ScrabbleCheater1.0/scrabbleWordsAndDef.txt")).read())
    # word = ""
    # listOfWords = []
    # 
    # for char in wordsList:
        # if char != "\n":
            # word = str(word) + str(char)
        # else:
            # listOfWords.append(str(word.lower()))
            # word = ""
    # wordAndDefList = []
    # 
    # for wordAndDef in listOfWords:
        # wordAndDefList += [wordAndDef.split("\t")]
    # 
    # definitions = []
    # 
    # wordsAndDefsSplit = []
    # 
    # for wordAndDef in tqdm(wordAndDefList):
        # word = str(wordAndDef[0])
        # definition = str(wordAndDef[1])
        # DefDbInput = Definitions(wordsToDefine=word, wordDefinition=definition) 
        # try:
            # db.session.add(DefDbInput)
            # db.session.commit()
        # except:
            # print("definition db didn't load properly...")
            # exit()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/scrabbler', methods=['GET', 'POST'])
def scrabbler():
    valid_words = ""
    if request.method == "POST":
        game_name = request.form['game_name']
        played_word = request.form['played_word']
        direction = request.form['direction']
        xcoord = request.form['xcoord']
        ycoord = request.form['ycoord']
        new_db_input = Scrabble(game_name=game_name, played_word=played_word, 
        direction=direction, xcoord=xcoord, ycoord=ycoord)
        letters = request.form['letters']
        if played_word != "":
            if xcoord != "":
                if ycoord != "":
                    try:
                        db.session.add(new_db_input)
                        db.session.commit()
                    except:
                        return "couldn't add to database..."

        board = initialise_board()
        data = Scrabble.query.filter_by(game_name=game_name).all()
        for x in data:
            if x.xcoord != "":
                board = play_move(True, board, x.played_word, x.xcoord, x.ycoord, x.direction)
        
        if letters != "":
            valid_words = wordRanker(wordScorer(wordFinder(letters, board)))

        return render_template('scrabbler.html',  board=board, game_name=game_name, valid_words=valid_words)

    else:
        board = initialise_board()
        return render_template('scrabbler.html', board=board)

@app.route('/scrabbler/definition_page', methods=['GET', 'POST'])
def definition_page():
    wordToDefine = request.form['wordToDefine']
    wordDefinition = Definitions.query.filter_by(wordsToDefine=wordToDefine).first()
    wordDefinition = wordDefinition.wordDefinition
    return render_template('definition_page.html', wordToDefine=wordToDefine, wordDefinition=wordDefinition)

if __name__ == "__main__":
    app.run(debug=True)

