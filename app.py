from flask import Flask, request, render_template, jsonify, session
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.route("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.route("/api/new-game")
def new_game():
    """Start a new game and return JSON: {gameId, board}."""

    # get a unique id for the board we're creating

    # generate game id
    gameId = str(uuid4())
    # instance of boggle game
    game = BoggleGame()
    # save instance to global set under game id generated
    games[gameId] = game

    return jsonify(gameId=gameId, board=game.board)


@app.route("/api/score-word", methods=["POST"])
def score_word():
    """ check if word is legal and return JSON response """
    # use JSON from request
    word = request.json["word"].upper()
    gameId = request.json["gameId"]

    # create instance of BoggleGame() with id
    game = games[gameId]

    # if not a word
    if not game.is_word_in_word_list(word):
        return jsonify(result="not_a_word")
    # if not on board
    elif not game.check_word_on_board(word):
        return jsonify(result="not_on_board")
    # valid word
    return jsonify(result="word_OK")
