from flask import Flask
from flask import session
from flask import render_template
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

# Play an action
@app.route("/action/<int:row>/<int:col>")
def action(row, col):
    if session["board"][row][col] is None:
        session["board"][row][col] = session["turn"]

    if session["turn"] == "X":
            session["turn"] = "O"
    else:
        session["turn"] = "X"

    return render_template(
        "board.html",
        board=session["board"]
    )

# DFS Cross
def dfs(board, row, col):
    stack = [] # probaly will continually reset the stack
    if board[row][col] == "X":
        stack.append((row, col))
    else:
        return True if len(stack) == 3 else False
    
    if row+1 < len(board):
        dfs(board, row+1, col)
    if row-1 >= 0:
        dfs(board, row-1, col)
    if col+1 < len(board[0]):
        dfs(board, row, col+1)
    if col-1 >= 0:
        dfs(board, row, col-1)
    
