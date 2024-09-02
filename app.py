from random import shuffle
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

CERTAIN_FOLDER = ""
RANDOM_MODE = "off"
SHUFFLE_LIST = []

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("password not match", 400)

        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES(?, ?)",
                request.form.get("username"),
                generate_password_hash(request.form.get("password")),
            )
            flash("register succeed!")
            return redirect("/")
        except:
            return apology("This username is picked", 400)

    else:
        return render_template("register.html")


@app.route("/decks", methods=["GET", "POST"])
def decks():
    if request.method == "POST":
        global CERTAIN_FOLDER
        if CERTAIN_FOLDER != "":
            CERTAIN_FOLDER = ""
        if request.form.get("folder_name"):
            CERTAIN_FOLDER = request.form.get("folder_name")
            return redirect("/cards")

        if request.form.get("delete_id") and request.form.get("delete") != None:
            folder = db.execute("SELECT folder FROM folder WHERE id = ?", request.form.get("delete_id"))[0]["folder"]
            db.execute("DELETE FROM cards WHERE folder = ?", folder)
            db.execute("DELETE FROM folder WHERE id = ?", request.form.get("delete_id"))
            return redirect("/decks")

        if request.form.get("folder_edit"):
            altefolder =  db.execute("SELECT folder FROM folder WHERE id = ?", request.form.get("id_edit"))[0]["folder"]
            db.execute("UPDATE folder SET folder = ? WHERE folder = ?", request.form.get("folder_edit"), altefolder)
            db.execute("UPDATE cards SET folder = ? WHERE folder = ?", request.form.get("folder_edit"), altefolder)
            return redirect("/decks")

        folder = request.form.get("folder")
        if not folder or folder == "Folder name":
            return apology("must provide folder name", 400)

        db.execute("INSERT INTO folder (user_id, folder) VALUES(?, ?)", session["user_id"], folder)
        return redirect("/decks")
    else:
        rows = db.execute("SELECT * FROM folder WHERE user_id = ?;", session["user_id"])
        return render_template("decks.html", rows=rows)


@app.route("/cards", methods=["GET", "POST"])
def cards():
    if request.method == "POST":
        if request.form.get("delete_id") and request.form.get("delete") != None:
            db.execute("DELETE FROM cards WHERE cards_id = ?", request.form.get("delete_id"))
            return redirect("/cards")

        if request.form.get("out") != None:
            return redirect("/decks")

        front = request.form.get("front")
        back = request.form.get("back")
        if not front:
            return apology("must provide front card", 400)
        elif not back:
            return apology("must provide back card", 400)

        if request.form.get("index") != "":
            db.execute("UPDATE cards SET front = ?, back = ? WHERE cards_id = ?", request.form.get("front"), request.form.get("back"), request.form.get("index"))
        else:
            db.execute("INSERT INTO cards (user_id, folder, front, back) VALUES(?, ?, ?, ?)", session["user_id"], CERTAIN_FOLDER, front, back)

        return redirect("/cards")
    else:
        rows = db.execute("SELECT * FROM cards WHERE user_id = ? AND folder = ?;", session["user_id"], CERTAIN_FOLDER)
        return render_template("cards.html", folder=CERTAIN_FOLDER, rows=rows)


@app.route("/list", methods=["GET", "POST"])
def list():
    if request.method == "POST":
        global CERTAIN_FOLDER
        if request.form.get("folder"):
            CERTAIN_FOLDER = request.form.get("folder")

        rows = db.execute("SELECT * FROM folder WHERE user_id = ?;", session["user_id"])
        cards = db.execute("SELECT * FROM cards WHERE user_id = ? AND folder = ?;", session["user_id"], CERTAIN_FOLDER)

        text = db.execute("SELECT notice FROM folder WHERE folder = ?", CERTAIN_FOLDER)[0]["notice"]
        if request.form.get("text") != None:
            db.execute("UPDATE folder SET notice = ? WHERE folder = ?", request.form.get("text"), CERTAIN_FOLDER)
            text = db.execute("SELECT notice FROM folder WHERE folder = ?", CERTAIN_FOLDER)[0]["notice"]

        if request.form.get("delete_id") and request.form.get("delete") != None:
            db.execute("DELETE FROM cards WHERE cards_id = ?", request.form.get("delete_id"))
            cards = db.execute("SELECT * FROM cards WHERE user_id = ? AND folder = ?;", session["user_id"], CERTAIN_FOLDER)

        if request.form.get("modal") != None:
            front = request.form.get("front")
            back = request.form.get("back")
            if not front:
                return apology("must provide front card", 400)
            elif not back:
                return apology("must provide back card", 400)
            if request.form.get("index") != "":
                db.execute("UPDATE cards SET front = ?, back = ? WHERE cards_id = ?", request.form.get("front"), request.form.get("back"), request.form.get("index"))
            else:
                db.execute("INSERT INTO cards (user_id, folder, front, back) VALUES(?, ?, ?, ?)", session["user_id"], CERTAIN_FOLDER, front, back)

            cards = db.execute("SELECT * FROM cards WHERE user_id = ? AND folder = ?;", session["user_id"], CERTAIN_FOLDER)

        return render_template("list.html", rows=rows, cards=cards, fol=CERTAIN_FOLDER, text=text)
    else:
        rows = db.execute("SELECT * FROM folder WHERE user_id = ?;", session["user_id"])
        return render_template("list.html", rows=rows)


@app.route("/learn", methods=["GET", "POST"])
def learn():
    if request.method == "POST":
        global CERTAIN_FOLDER
        global RANDOM_MODE
        global SHUFFLE_LIST

        if request.form.get("folder"):
            CERTAIN_FOLDER = request.form.get("folder")

        rows = db.execute("SELECT * FROM folder WHERE user_id = ?;", session["user_id"])
        cards = db.execute("SELECT * FROM cards WHERE user_id = ? AND folder = ?;", session["user_id"], CERTAIN_FOLDER)

        if request.form.get("out") != None:
            return redirect("/learn")

        # argument unpacking operator * to unpackt the range()
        if request.form.get("random") != None:
            RANDOM_MODE = "on"
            temp = [*range(len(cards))]
            shuffle(temp)
            SHUFFLE_LIST = temp

        if request.form.get("normal") != None:
            RANDOM_MODE = "off"

        index = 0
        if request.form.get("next") != None:
            cards = db.execute("SELECT * FROM cards WHERE user_id = ? AND folder = ?;", session["user_id"], CERTAIN_FOLDER)
            index = int(request.form.get("index")) + 1

        if request.form.get("prev") != None:
            cards = db.execute("SELECT * FROM cards WHERE user_id = ? AND folder = ?;", session["user_id"], CERTAIN_FOLDER)
            index = int(request.form.get("index")) - 1

        return render_template("learn.html", rows=rows, cards=cards, fol=CERTAIN_FOLDER, index=index, random=RANDOM_MODE, shuffle=SHUFFLE_LIST)
    else:
        RANDOM_MODE = "off"
        rows = db.execute("SELECT * FROM folder WHERE user_id = ?;", session["user_id"])
        return render_template("learn.html", rows=rows)