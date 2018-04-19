from flask import Flask, url_for, request
from flask import render_template
from board import Board
from solver import solve

app = Flask(__name__)

@app.route('/')
def index():
    # If request.args has items, but not 81 of them, it's likely that someone appended
    #   invalid values to the URL.
    # It's possible that someone just specified some of the cells and left the rest out
    #   of the argument list, but I don't see value in catering to that possibility.
    if not request.args or len(request.args) != 81:
        print "Didn't find a request."
        return render_template('grid.html')
    board_letters = []
    for row in xrange(9):
        for col in xrange(9):
            cell = request.args.get(str(row) + str(col), '')
            if cell == "" or cell == "0":
                board_letters.append("0")
            else:
                board_letters.append(cell)
    board_array = Board.string_to_array("".join(board_letters))
    b = Board(board_array)
    try:
        solved = solve(b)
    except ValueError as e:
        msg = str(e) + " Please try entering your board values manually."
        return render_template('grid.html', error=msg)
    return render_template('result.html', output=solved.to_dict())