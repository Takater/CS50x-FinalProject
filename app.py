from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
import requests, json
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, validate_pwd, reward, User, Trivia as tv, Gameplay as gp, Hangman as hang

# Application config
app = Flask(__name__)

# Database config
db = SQL("sqlite:///game.db")

# Auto-reloaded templates
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Session uses filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Route to search for existing username on 'REGISTER.HTML' JSON fetch
@app.route("/search")
def search():
    user = db.execute("SELECT * FROM users WHERE username = ?", request.args.get('username'))
    if len(user) != 0:
        return user[0]
    else:
        return "404"

# User registration page
@app.route("/register", methods=["GET", "POST"])
def register():

    # POST method
    if request.method == "POST":

        # Get form fields
        username = request.form.get("username")
        pwd = request.form.get("password")
        conf = request.form.get("confirmation")

        # Check if user answered all fields
        if not username or (not pwd) or (not conf):
            return render_template("register.html", message="There are missing information")

        # Validate information
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        match = (validate_pwd(pwd) and (pwd == conf))
        if len(user) !=0 or len(username) < 6 or not match:
            return render_template("register.html", message="Invalid information provided")

        # Add user to database and go to login page
        db.execute("INSERT INTO users (username, pw_hash) VALUES (?, ?)", username, generate_password_hash(pwd))
        return redirect("/login")

    # GET method
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # POST method
    if request.method == "POST":

        # Ensure user typed username
        if not request.form.get("username"):
            return render_template("login.html", message_usr = "Missing username")

        # Ensure user typed password
        if not request.form.get("password"):
            return render_template("login.html", message_pw = "Missing password")

        # Ensure username exists and password is correct
        user = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(user) == 0:
            return render_template("login.html", message_usr = "Username doesn't exist")
        else:
            password = request.form.get("password")
            if not check_password_hash(user[0]["pw_hash"], password):
                return render_template("login.html", message_pw = "Wrong password")

        # Login user
        session["user_id"] = user[0]["id"]

        # Open home page
        return redirect("/")

    # GET method
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    # Forget user id
    session.clear()

    # Send back to home page
    return redirect('/')

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    # User info for navbar
    user = User(session["user_id"])

    # POST method (User changed AVATAR)
    if request.method == "POST":
        avatar_id = int(request.args.get('avatar'))
        avatar = db.execute("SELECT title FROM store WHERE productId = ? AND productId IN (SELECT product_id FROM purchases WHERE user_id = ?)", avatar_id, user.id)[0]['title']
        db.execute("UPDATE users SET avatar = ? WHERE id = ?", avatar, user.id)
        return redirect('/')

    # GET method
    else:
        # Open home page with User's info
        return render_template("index.html", user=user)

@app.route('/profile')
@login_required
def profile():

    # User info for navbar and tables
    user = User(session["user_id"])

    # Info for tables
    matches = db.execute("SELECT * FROM matches WHERE user_id = ? ORDER BY date DESC", user.id)
    games = db.execute("SELECT * FROM games")
    store = db.execute("SELECT * FROM store")

    # Return template
    return render_template("profile.html", user=user, matches=matches, games=games, store=store)

@app.route('/store', methods=["GET", "POST"])
@login_required
def store():

    # User info for navbar
    user = User(session["user_id"])

    # Store info for table
    store = db.execute("SELECT * FROM store")

    # POST method (User confirmated purchase)
    if request.method == "POST":

        # Ensure info was passed
        title = request.args.get("title")
        if not title:
            return render_template("store.html", user=user, store=store)

        else:

            # Update user's coins and add acquisition to user's purchases
            product = db.execute('SELECT * FROM store WHERE title = ?', title)[0]
            user.update(coins = -(product['price']))
            user.purchase(product)

            # Redirect back to Store page
            return redirect('/store')

    # GET method
    else:
        return render_template("store.html", user=user, store=store)

#######################################################################################
####                                                                               ####
####   #############    #########    ####     ####  #############  #############   ####
####   ##              ##       ##   ## ##   ## ##  ##             ##              ####
####   ##   ########  ##         ##  ##  ## ##  ##  ##             ##              ####
####   ##   ##    ##  #############  ##   ###   ##  ###########    #############   ####
####   ##         ##  ##         ##  ##         ##  ##                        ##   ####
####   ##         ##  ##         ##  ##         ##  ##                        ##   ####
####   #############  ##         ##  ##         ##  #############  #############   ####
####                                                                               ####
#######################################################################################

# TRIVIA INDEX
@app.route("/trivia")
@login_required
def trivia():

    # User info for navbar
    user = User(session["user_id"])

    # Categories list for select
    categories_dict = (json.loads((requests.get('https://opentdb.com/api_category.php').text)))['trivia_categories']
    categories = []
    for row in range(len(categories_dict)):
        categories.append(categories_dict[row]['name'])

    return render_template("trivia.html", user=user, categories=categories)


# TRIVIA QUESTIONS
@app.route('/trivia/question', methods = ["GET", "POST"])
@login_required
def question():

    # Row count from second question on (Index #1 for questions dictionary)
    current_question = request.args.get("row")

    # User info for navbar
    user = User(session["user_id"])

    # If it's the first question
    if not current_question:

        # Get info from Trivia form for questions
        number = int(request.form.get("number"))
        theme = request.form.get("category")
        diffic = request.form.get("difficulty").lower()
        if not number or not theme or not diffic:
            return redirect("/trivia")

        # Object for questions
        global questions_dict
        questions_dict = tv.question_dict(number=number, category=theme, difficulty=diffic)
        if questions_dict == "Not found":
            return redirect("/trivia")

        # JSON variables (Total and current questions)
        global rows, row
        rows = json.dumps(int(number))
        row = json.dumps(1)

        # Return first question
        return render_template("question.html", questions_dict=questions_dict[0], user=user, rows=rows, row=row)

    # If it's not the first question
    elif int(current_question) < (len(questions_dict)):

        # Row from questions dict (Index #1 through #lenght - 1)
        current_question = int(current_question)

        # Current question for template
        row = json.dumps(current_question + 1)

        # Return current question template
        return render_template("question.html", questions_dict=questions_dict[current_question], user=user, rows=rows, row=row)

    # If last question has been answered
    else:
        current_question = int(current_question)
        row = json.dumps(current_question + 1)

        # Get correct answered questions
        answers = db.execute('SELECT answers FROM matches WHERE user_id = ? ORDER BY date DESC', session["user_id"])[0]['answers']

        # Calculate reward
        rwd = reward(questions_dict[0]['difficulty'], answers)

        # Update user with rewards
        user.update(coins = rwd['coins'], xp = rwd['xp'])

        # Return template with correct answered questions and rewards
        return render_template("question.html", questions_dict=questions_dict[current_question - 1], user=user, rows=rows, row=row, answers=answers, rewards=rwd)

@app.route('/hangman', methods=["GET", "POST"])
@login_required
def hangman():
    # User info for navbar
    user = User(session["user_id"])

    # Variables sent via URL when game finishes
    answers = request.args.get("answers")
    result = request.args.get("result")

    # If user clicked "GENERATE WORD"
    if request.method == "POST" and not answers:

        # Difficulty from form
        global difficulty
        difficulty = request.form.get("difficulty").lower()

        # Generate word and alphabet for template
        word = hang.get_word(difficulty)
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        abc = json.dumps(alphabet)
        curr_word = json.dumps(str(word))

        # Return word
        return render_template("hangman.html", user=user, word=word, alphabet=alphabet, abc=abc, curr_word=curr_word)

    # If user finished the game
    elif request.method == "POST" and answers:

        # Get match_id
        curr_match = db.execute("SELECT id FROM matches WHERE user_id = ? and game_id = 2 ORDER BY date DESC", user.id)[0]["id"]

        # Update user's answers, calculate reward and update users coins and xp
        db.execute("UPDATE matches SET answers = ? WHERE id = ?", answers, curr_match)
        rwd = reward(difficulty, round(float(answers)))
        user.update(coins = rwd['coins'], xp = rwd['xp'])

        # Render template with reward info
        return render_template("hangman.html", user=user, answers=answers, result=result, rewards=rwd)

    # GET method (from index)
    else:
        return render_template("hangman.html", user=user)

# Route to generate Gameplay Object

@app.route('/match')
@login_required
def match():
    # Get game and difficulty and create global Obj variable
    game = request.args.get('game')
    diff = request.args.get('difficulty')
    global gameplay

    # Create object based on chosen game
    if request.args.get('start') and game == 'Trivia':
        gameplay = gp(session["user_id"],'Trivia', diff)

    if request.args.get('start') and game == 'Hangman':
        gameplay = gp(session["user_id"], 'Hangman', diff)

    # Correct question counter for Trivia
    if request.args.get('correct'):
        answers = db.execute('SELECT answers FROM matches WHERE user_id = ? AND game_id = ? AND date = ?',gameplay.user_id, gameplay.game_id, gameplay.time)[0]['answers']
        answers += int(request.args.get('correct'))
        gameplay.match(answers)
        return '0'

    return '0'
