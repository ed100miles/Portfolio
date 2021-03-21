from datetime import datetime
from flask import Flask, render_template, request, redirect
from  Scrabbler import initialise_board, wordFinder, wordScorer, wordRanker, play_move
from flask_sqlalchemy import SQLAlchemy
import csv
from tqdm import tqdm
import datetime as dt
from bokeh.plotting import figure, show, save, output_file
from bokeh.embed import components
import bokeh.layouts
from bokeh.resources import CDN
from scipy.ndimage.filters import gaussian_filter1d
import dateutil
import numpy as np

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

@app.route('/catSpot')
def catSpot():
    csvPath = 'static/csvs/catSpots.csv'
    csvFile = open(csvPath, newline='')
    reader = csv.reader(csvFile)
    data = []
    previous_spots = []

    for row in reader:
        if len(row) > 1:
            data.append(row)
    data.reverse()
    
    for x in data:
        spotTime, confidence = x
        spotTime = round(float(spotTime))
        spotTime = datetime.utcfromtimestamp(int(spotTime)).strftime('%d-%m-%Y %H:%M:%S')
        roundConf = float(confidence)*100
        roundConf = round(roundConf, 2)
    
    previous_spots.append(f'Spotted at: {spotTime}, Confidence: {roundConf}%')
    lastCatSpot = previous_spots.pop(0)

    return render_template('catSpot.html', lastCatSpot=lastCatSpot, previous_spots=previous_spots)

@app.route('/sentiment')
def sentiment():
    csvfile = 'static/csvs/tweet_out.csv'

    graph_data = open(csvfile, 'r').read()
    lines = graph_data.split('\n')

    xs = []
    ys_mean = []

    bias_skew = 0.15
    smoothing = 250

    for num, line in enumerate(lines[200:]):
        if len(line) > 1:
            if num % 1 == 0:
                x, y_mean, pos, neg, sent  = line.split(',')
                x_dt = dt.datetime.utcfromtimestamp(float(x))
                xs.append(x_dt)
                ys_mean.append(((float(y_mean))-bias_skew)*100)
            
    ys_mean = np.asarray(ys_mean)
    ys_mean_smooth = gaussian_filter1d(ys_mean, sigma=smoothing)

    p = figure(title="Sentiment",
                x_axis_label='Time',
                x_axis_type='datetime',
                y_axis_label='Joe Biden Sentiment%',
                plot_width=1000,
                plot_height=500)

    ys_mean_smooth_pos = []
    ys_mean_smooth_neg = []
    for x in ys_mean_smooth:
        if x > 0:
            ys_mean_smooth_pos.append(x)
            ys_mean_smooth_neg.append(0.0)
        else:
            ys_mean_smooth_pos.append(0.0)
            ys_mean_smooth_neg.append(x)

    p.varea(x=xs,
            y1=0,
            y2=ys_mean_smooth_pos,
            fill_color='green',
            fill_alpha=0.3)

    p.varea(x=xs,
            y1=0,
            y2=ys_mean_smooth_neg,
            fill_color='red',
            fill_alpha=0.3)            
    
    p.line(xs, ys_mean_smooth, legend_label='Mean Sentiment', line_width=2)

    p.sizing_mode="scale_width"

    script, div = components(p)
    bok_css = CDN.css_files
    bok_js = CDN.js_files
    bok_css = bok_css
    bok_js = bok_js[0]

    return render_template('sentiment.html', script=script, div=div, bok_css=bok_css, bok_js=bok_js)

if __name__ == "__main__":
    app.run(debug=True)

