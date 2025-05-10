from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'boggle-secret'
app.debug = True
toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def homepage():
    """Display board and game interface."""
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('board.html', board=board)

@app.route('/check-word')
def check_word():
    """Check if submitted word is valid."""
    word = request.args.get('word', '').lower()
    board = session.get('board')
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result': result})

@app.route('/post-score', methods=['POST'])
def post_score():
    """Receive and record score, update high score and times played."""
    score = request.json.get('score', 0)
    times_played = session.get('times_played', 0) + 1
    high_score = max(score, session.get('high_score', 0))
    session['high_score'] = high_score
    session['times_played'] = times_played
    return jsonify(high_score=high_score, times_played=times_played)

