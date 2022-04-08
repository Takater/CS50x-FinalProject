# GAME ZONE

## CS50x Final Project
### Video Demo: [GAMEZONE Video](https://youtu.be/PL1tLJnBg6E)
#
## DESCRIPTION:
### **1. What is it?**
#### _GAMEZONE_ is a Web Application with registration/login requirement where the user can play different 'word games', currently: Trivia and Hangman, to gather XP and Coins to level up and buy various 'pictures' or 'avatars' for oneself's profile.
#
### **2. How was it implemented?**
#### **2.1 - Markup, Styling. Programming, Database and Framework:**
#### _GAMEZONE_ was made with **Flask** micro-Framework on CS50's Codespace, integrating:
• Frontend: **HTML**, **CSS**, **JavaScript** (with **JSON**) and **Jinja** templating engine.<br>
• Backend: **Python** and **SQLite**.
#### **2.2 - APIs, Libraries and Modules:**
##
####  <u>**Libraries**:</u>
#### • **CS50**: Library used for SQL module.
#### • **Flask**: Library used for running the Web App properly: rendering HTML templates, redirecting the user, requesting form inputs or URL arguments and keeping track of user actions (session cookies).
#### • **Werkzeug.security**: Library used to encrypt and decrypt passwords troughout the Application and Database.
#### • **Functools**: Library used for a decorated function to require login on certain _App_ routes.
#### • **Re**: Library used to compile a RegEx and compare it to the password chosen by the user to validate it for registration.
#### • **Bootstrap**: Library used in this project for styling and manipulating HTML templates.
#### <u>**Modules**:</u>
#### • **Requests and JSON modules**: Modules used to pass backend variables values to frontend variables.
#### • **Random module:** Module used to get random words or randomly shuffle numbers.
#### • **Html module:** Module used to fix strings with HTML entities
####
#### <u>**APIs**:</u>
#### • [Opentdb](https://opentdb.com/) : API used to develop Trivia game. It's used in _GAMEZONE_ to retrieve categories for user's choice, and a Python list of dictionaries with questions and answers.
#### • [Random Word](https://random-word-api.herokuapp.com/) : API used to develop Hangman game. A text file called _'word.txt'_ was generated with 500.000 words from this API, a module is used to retrieve one random word from this file.
#### • [Dictionary](https://dictionaryapi.dev/) : API to retrieve word definition for Hangman game.
#
### **3. Game.db**
##
#### _GAMEZONE_ is implemented with a SQLite database called game.db which has 5 (five) tables: **users**, **games**, **store**, **matches**, and **purchases**. All tables have a PRIMARY KEY column with sometype of ID.
#### • **<u>users</u>** : user's data, information in columns: **ID**, **username**, the **password hash** (encrypted), amount of **coins**, current amount of **XP**, necessary **XP for next level**, current **level** and current **avatar** in use.
#### • **<u>games</u>** : current existing games in _GAMEZONE_, information in columns: game **ID**, game **name**.
#### • **<u>store</u>** : keep store's products data, information in columns: **product ID**, **price**, **title**. As products are images, the **title** is the file name of the image (e.g. 'av1.png').
#### • **<u>matches</u>**: keep track of played matches for all users, information in columns: match **ID**, **user id** (FOREIGN KEY from _users_ table), **game id** (FOREIGN KEY from _games_ table), number of calculated **answers** for current match (it is used to dinamically calculate rewards), the **difficulty** chosen by the user (also used for reward calculation), the **date** and time when the match was started (used for profile history).
#### • **<u>purchases</u>** : keep track of products acquired by users, information in columns: purchase **ID**, **product ID** (FOREIGN KEY from _store_ table), product **price**, **user id** (FOREIGN KEY from _users_ table), the **date** and time of purchase (used for profile history).
#
### **4. Folders, CSS files and HTML templates**
##
#### _GAMEZONE_ has 3 (three) main folders, ***~/project*** is the root folder for the whole WebApp, it contains the ***Python files***(.py) used, the database (***game.db***) used, this ***README*** file, 2 (two) text files called ***requirements.txt*** and ***words.txt*** (the last one is used for _Hangman_ game).
#### The ***project/static*** directory contains _favicons_, _CSS files_, and 2 (two) other folders: **/*images***, with the .png images for _Hangman_ game; and ***/store***, with the .png images for the _store_'s avatars.
#### The ***project/templates*** directory contains all HTML templates used in the _App_.
##
#### **4.1 - CSS files:**
#### • **<u>styles.css</u>** : CSS file used on _layout_ page (***layout.html***) for pages before a user has logged in.
#### • **<u>index_style.css</u>** : CSS file used on _layout_ page (***homepage.html***) for pages after user has logged in.
##
#### **4.2 - HTML templates:**
#### This project has 10 (ten) HTML templates, including 2 (two) _layout_ templates, 2 templates for when no user is logged in, 3 templates for user navigation when logged in, and 3 templates for the games.
##
#### **4.2.1 - Layout templates:**
#### • <u>***layout.html***</u> : A navbar with _Register_ and _Login_ buttons, and a static background.
#### • <u>***homepage.html***</u> : A navbar with user information – username, coins, a bar to indicate current XP percentage before next level, current level and avatar – and _Profile_, _Store_ and _Logout_ buttons; and an animated background effect gotten from [here](https://codepen.io/donovanh/pen/qmNgXW) with a few changes made. Featured with a modal opened on avatar click to show user's available avatars and allow user to change it.
#### **4.2.2 - Before-login templates:**
#### • <u>***register.html***</u> : a registration form with 3 (three) fields: _username_, _password_ and _password confirmation_. Featured with on-input checking: if username is already in use, if password fits requirements and if confirmation field and password fields are the same.
#### • <u>***login.html***</u> : a log in form with 2 (two) fields: _username_ and _password_. Featured with: JSON fetch to check if username exists and if username and password match.
#
#### **INFORMATION FROM FORM FIELDS FOR ABOVE TEMPLATES ARE VALIDATED BOTH IN FRONTEND AND BACKEND.**
##
#### **4.2.3 - After-login templates:**
#### • <u>***index.html***</u> : the so-called homepage for the user, with images/links to the games below the layout's navigation bar.
#### • <u>***profile.html***</u> : page with tables for _matches_ and _purchases_ history for that user. Featured with a on-change dropdown selection button to select which tables to show.
#### • <u>***store.html***</u> : page with a table with all available products from _store_ table, including the images and prices. Featured with a on-change dropdown selection button to select which type of avatars to show and modals on "BUY" buttons to confirm purchases.
##
#### **4.2.4 - Games templates:**
#### • <u>***trivia.html***</u> : page with a form with 3 (three) buttons to select game guidelines: number of questions, category and difficulty, and a button to submit the form and start the game.
#### • <u>***question.html***</u> : page opens firstly with a form including a Trivia's question, 4 possible answers and a button to go to next question (or finish when gets to last question). Featured with: showing the user if correct answer has been chosen by changing backgroud and text color (using Bootstrap classes) for correct answer and/or chosen answer; a countdown clock of 15 seconds for the user to answer the question, if the user fails to answer within the time it goes automatically to next question. After user answers last question, page shows how many correct answers the user had and the rewards for that match.
#### • <u>***hangman.html***</u> : page opens firstly with a one-field-form with a dropdown selection for user to choose the difficulty for the game, and a button to get a random word from that difficulty level. After user chooses and click the button, page shows the empty fields for each letter of the word, a definition for the word (if found) and 26 buttons for each of the Alphabet letters. After user wins (answers all letters) or loses (6 (six) mistakes) the page opens an overlay container with the result and the rewards for that match and a button for a _"NEW GAME"_. Featured with: Printing correct number of fields for each letter in the generated word, get definition for word through [this dictionary API](https://dictionaryapi.dev/), change hang image according to wrong answers (including parts of the body), show overlay container with results.
#
### **5. Python files**
#### _GAMEZONE_ was implemented with 2 (two) '_~.py_' files: ***app.py***, which uses Flask framework to call routes to render each _.html_ template with its specific guidelines; and ***helpers.py***, which contains functions and classes to be used throughout _app.py_.
#
#### **5.1 - Helpers.py:**
#### **5.1.1 - Functions:**
#### • **<u>login_required</u>** : this function was based on a previous problem set from CS50 (Finance) to generate a decorated function to require that a user is logged in, in order to access a route.
#### • **<u>validate_pw</u>** : this function was implement with _Re_ library to ensure that the user followed password creation requirements when registrating.
#### • **<u>reward</u>** : this function requires 2 (two) arguments (difficulty and answers) and dinamically calculate a reward based on the arguments received.
#### **5.1.2 - Classes:**
#### • **<u>User</u>** : class to carry and manipulate the user's data through routes. It is initialized by _session['user_id']_ and get the information from _users_, _store_, and _purchases_ tables.
#### It has 2 (two) inner functions:
#### - <u>*update*</u> : function to update user's coins, and/or xp and level. It requires as argument a variable-length dictionary (**kwargs) to allow updating both coins and xp or only one of them.
#### - <u>*purchase*</u> : function to update purchases database to include user's acquisitions from store. It requires as argument a dictionary (product) that includes the _productId_ and _price_ (from _store_ table).
#
#### • **<u>Gameplay</u>** : class to generate and manipulate a row from _matches_ table. It is initialized with _session['user_id']_, _game_name_ and _difficulty_ to create a row and it has 1 (one) inner function:
#### - <u>*match*</u> : this functions requires one argument (answers) and update the current match _answers_ column accordingly. This is mainly used to calculate _reward_ correctly.
#
#### • **<u>Trivia</u>** : class with one single function to properly return a list of dictionaries with questions and answers from [OPENTDB API](https://opentdb.com/) according to user's choices (number of questions, difficulty, category).
##
#### • **<u>Hangman</u>** : class with one single function to properly return a random word from _'words.txt'_ file according to user's difficulty choice.
#
#### **5.2 - App.py:**
#### This file contains the 'main' _app_ functions. It uses Flask to start and configure the _app_, the routes handle both or one method ("GET" and/or "POST"). If a route is ***login_required***, it first initializes a variable called _users_ with _Users_ class. ***App.py*** has 11 (eleven) **routes** :
##
#### **5.2.1** - ***<u>('/search')</u>*** : this route purpose it to be used on a JSON fetch asynchronous function on an _.html_ template ( _register.html_ ) to search and check if a user exists within the database and therefore ensure usernames are unique.
#### **5.2.2** - ***<u>('/register')</u>*** : this route handles both methods. When called on "GET" it renders ***register.html*** template. When called on "POST" it gets the information from the template's form fields, validates the information – if any information is not valid it renders the template with a message for the user – , adds user to _users_ table and redirects the user to ***login*** route.
#### **5.2.3** - ***<u>('/login')</u>*** : this route handles both methods. When called on "GET" it renders ***login.html*** template. When called on "POST" it gets the information from the template's form fields, checks and validates the information – if any information is not valid it renders the template with messages for the user – , logins and redirects the user to **index**.
#### **5.2.4** - ***<u>('/logout')</u>*** : this route logouts the user by clearing the session, and then redirects to ***login*** route.
#### **5.2.5** - ***<u>('/')</u>*** : this is the ***index*** route, it is ***login_required***, and handles both methods. When called on "GET" method it renders ***index.html*** with user's information. It's called on "POST" when the user changes the avatar: the avatar_id (_productId_ in _store_ table) is sent via URL argument, its _title_ is gotten from _store_ table and it's updated on _users_ table. Then, the user is redirected to ***index***.
#### **5.2.6** - ***<u>('/profile')</u>*** : this route is ***login_required***, it handles only "GET" method and renders ***profile.html*** template with: _user's_ information, all _matches_ played by the user, and the _store_ table to generate the images based on _users.purchases_.
#### **5.2.7** - ***<u>('/store')</u>*** : this route is ***login_required***, besides user's information, it also initializes a "_store_" variable with the information from _store_ table. It handles both methods. When called on "GET", it renders ***store.html*** template with _store_ variable. It's called on "POST" when the user chooses and confirms choice for acquisition, it gets the product information from _store_ table and updates user coins and purchases.
#### **5.2.8** - ***<u>('/match')</u>*** : this route is ***login_required*** but it doesn't start a _User_ class. It's called on JSON asynchronous functions on games' templates to generate and manipulate _matches_ table rows through _Gameplay_ class.
#### **5.2.9** - ***<u>('/trivia')</u>*** : this route is ***login_required***, it handles "GET" method only and renders ***trivia.html*** template with _user's_ information and the _categories list_ from [OPENTDB API](https://opentdb.com/) for a dropdown selection input.
#### **5.2.10** - ***<u>('/trivia/question')</u>*** : this route is ***login_required***, it handles both methods but it's called only on "POST". It renders ***question.html*** template again and again for a **Trivia** match. First building a list of questions and answers through _Trivia_ class, then it dinamically renders the template with the current question (using json module) and when the last question is answered it calculates the reward for that match, updates user's coins and XP, and renders the template showing the rewards gained.
#### **5.2.11** - ***<u>('/hangman')</u>*** : this route is ***login_required***, it handles both methods. Besides user's information it initially starts variables with URL arguments (answers and results) to check if user started or finished the game. When called on "GET" it renders ***hangman.html*** template with _user's_ information. When called on "POST" (user chose difficulty) it checks which URL arguments were sent, if no answers were sent it means the game has just started and renders the template with a random word based on user's choice (from _Hangman_ class) and some variables to be used (using json module); if answers were sent (and therefore the result: win or lose) it means the game has finished so it calculates the reward based on the answers, updates user's coins and XP and renders the template with rewards and result information.
#
#
## This was CS50x.
### <u>Project by</u>: Guilherme Moret
### <u>Location</u>: Porto Velho, Rondônia, Brasil