from flask import redirect, session
from functools import wraps
from cs50 import SQL
import requests, json, random, html

# Database config
db = SQL("sqlite:///game.db")

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def validate_pwd(pwd):

    # Import 're' library and compile regex to pattern
    import re
    regex = '^((?=.*\d)|(?=.*[!@#$%^&*]))((?=.*[a-z])|(?=.*[A-Z])).{6,15}$'
    pattern = re.compile(regex)

    # Checking match
    if not re.search(pattern, pwd) or not pwd[0].isalpha():
        return False
    else:
        return True

# Generate reward based on user's difficulty choice and answers
def reward(difficulty, answers):
    base = 0
    if difficulty == 'easy':
        base = 50
    if difficulty == 'medium':
        base = 100
    if difficulty == 'hard':
        base = 150
    coins = base * answers
    xp = round(50 * answers * ((base/50) + 1))
    reward = {'coins': coins, 'xp': xp}
    return reward

# User object (Generated on routes)
class User:
    def __init__(self, id):
        user = db.execute("SELECT * FROM users WHERE id = ?", id)[0]
        self.id = id
        self.name = user['username']
        self.coins = user['coins']
        self.level = user['level']
        self.xp = user['xp']
        self.xp_next = user['xp_next']
        self.avatar = user['avatar']
        self.percentage = (self.xp/self.xp_next) * 100
        self.purchases = db.execute("SELECT * FROM purchases WHERE user_id = ? ORDER BY product_id", self.id)
        self.avatars = db.execute("SELECT title FROM store WHERE productId in (SELECT product_id FROM purchases WHERE user_id = ?) ORDER BY productId", self.id)

    # User function to update coins and/or xp and level
    def update(self, **update):
        coins = self.coins
        xp = self.xp
        try:
            coins += update['coins']
        except KeyError:
            coins = self.coins
        try:
            xp += update['xp']
        except KeyError:
            xp = self.xp
        if xp >= self.xp_next:
            xp = xp - self.xp_next
            self.level += 1
            self.xp_next += round((self.xp_next*0.1) + self.xp_next)
        db.execute('UPDATE users SET coins = ?, xp = ?, xp_next = ?, level = ? WHERE id = ?', coins, xp, self.xp_next, self.level, self.id)

    # User function to keep track of products' acquisition from store
    def purchase(self, product):
        db.execute("INSERT INTO purchases(product_id, price, user_id) VALUES(?, ?, ?)", product['productId'], product['price'], self.id)

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

# Object to generate Trivia's questions
class Trivia:
    def question_dict(**kwargs):

        # Get variables
        number = kwargs['number']
        type = '&type=multiple'
        theme = kwargs['category']
        diffic = kwargs['difficulty']
        cat = '&category='
        dif = ""
        if diffic != "":
            dif =  '&difficulty=' + diffic
        if theme == "Random":
            cat = ""
        else:

            # Clean string to search correctly
            if theme.find('&amp;') != -1:
                theme = theme.replace('&amp;', '&')

            # Get category ID for URL if not random
            categories_dict = (json.loads((requests.get('https://opentdb.com/api_category.php').text)))['trivia_categories']
            for row in range(len(categories_dict)):
                if categories_dict[row]['name'] == theme:
                    cat = cat + str(categories_dict[row]['id'])

        # Get questions from OPEN TRIVIA DB
        url = 'https://opentdb.com/api.php?amount=' + str(number) + cat + dif + type
        questions_dict = (json.loads(requests.get(url).text))
        if questions_dict['response_code'] != 0:
            return "Not found"
        questions_dict = questions_dict['results']

        # Build questions-dicts list
        questions_list = []
        for row in range(len(questions_dict)):
            each = questions_dict[row]

            # List of answers
            answers = []
            correct_answer = each['correct_answer']
            answers.append(correct_answer)
            for answer in range(3):
                answers.append(each['incorrect_answers'][answer])
            random.shuffle(answers)

            # Fix 'html' unicodes in questions
            if '&' in each['question']:
                ind = each['question'].find('&')
                fin = each['question'].find(';')
                string = each['question'][ind:fin + 1]
                code = html.unescape(string)
                each['question'] = each['question'].replace(string, code)

            # Row for each question
            questions_list.append({'row': row + 1, 'rows': number,'theme': each['category'], 'difficulty': each['difficulty'],'question': each['question'], 'correct': each['correct_answer'], 'answers': answers})

        # Return dictionary
        return questions_list

# Object to generate Hangman's words
class Hangman:
    def get_word(diff):

        # Open and read file with words
        with open("words.txt", "r") as file:
            every_word = file.read()

            # List with all words
            words = list(map(str, every_word.split(",")))

            # Choose random word based on user's difficulty choice
            word = random.choice(words)
            if diff == "easy":
                while len(word) > 5 or len(word) <= 2:
                    word = random.choice(words)
            elif diff == "medium":
                while len(word) > 8 or len(word) <= 5:
                    word = random.choice(words)
            elif diff == "hard":
                while len(word) > 12 or len(word) <= 8:
                    word = random.choice(words)

            # Clean quote marks from word
            word = word.replace("\"", "")

        # Return word
        return word

# Object for matches played by user
class Gameplay:
    def __init__(self, id, game_name, difficulty):

        # Game and user info
        self.game_id = db.execute('SELECT id FROM games WHERE game_name = ?', game_name)[0]['id']
        self.user_id = db.execute('SELECT id FROM users WHERE id = ?', id)[0]['id']

        # Insert into MATCHES table
        db.execute('INSERT INTO matches(user_id, game_id, difficulty) VALUES(?, ?, ?)', self.user_id, self.game_id, difficulty)

        # Get time and id of current match
        self.time = db.execute('SELECT date FROM matches WHERE user_id = ? AND game_id = ? ORDER BY date DESC', self.user_id, self.game_id)[0]['date']
        self.match_id = db.execute('SELECT id FROM matches WHERE user_id = ? AND game_id = ?', self.user_id, self.game_id)[0]

    # Function to update answers result from user's match
    def match(self, answers):
        db.execute('UPDATE matches SET answers = ? WHERE user_id = ? AND game_id = ? AND date = ?', answers, self.user_id, self.game_id, self.time)