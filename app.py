from flask import Flask
from flask import session
from flask import render_template
from flask import redirect
from flask import url_for
from flask_session import Session
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

# Set the board
@app.route("/set")
def base():
    if "board" not in session:
        session["turn"]   = "X"
        session["winner"] = False
        session["board"]  = [[None, None, None], [None, None, None],[None, None, None]]
    
    return render_template(
        "board.html",
        board=session["board"]
    )

# Reset the board
@app.route("/reset")
def reset():
    session["turn"]   = "X"
    session["winner"] = False
    session["board"]  = [[None, None, None], [None, None, None],[None, None, None]]

    return redirect(url_for("base"))

# Play an action
@app.route("/action/<int:row>/<int:col>")
def action(row, col):
    player = session["turn"]
    if session["board"][row][col] is None:
        session["board"][row][col] = session["turn"]
    
    result = is_winner(session["board"], session["turn"])

    if session["turn"] == "X":
            session["turn"] = "O"
    else:
        session["turn"] = "X"

    if result == False:
        return render_template(
        "board.html",
        board=session["board"]
    )
    else:
        return render_template(
        "winner.html",
        board=session["board"],
        player=player
    )

def is_winner(board, turn):
    n = len(board)
    for indexes in win_cons(n):
        if all(board[r][c] == turn for r, c in indexes):
            return True
    return False

def win_cons(n):
    # Rows
    for r in range(n):
        yield [(r, c) for c in range(n)]

    # Columns
    for c in range(n):
        yield [(r, c) for r in range(n)]

    # Diagonal top left to bottom right
    yield [(i, i) for i in range(n)]

    # Diagonal top right to bottom left
    yield [(i, n - 1 - i) for i in range(n)]
