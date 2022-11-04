from flask import Flask, render_template, request, redirect, make_response
from flask_socketio import SocketIO, send, emit
import requests, os, random
from functools import partial
from database import Database
from users import UserPage 

def random_code():
  letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s","t", "u", "v", "w", "x", "y", "z"]

  string = ""
  for i in range(1, 9):
    r = random.choice(letters)
    if random.randint(1,2) == 1:
      r = r.upper()
    string = string + r
  return string
BASE = "https://quacker-api.theprogrammerking.repl.co/"
# post.new_post()
# request = requests.put(BASE+f"posts/{random_code()}", {"username": "money", "text":"first ever post"})
# print(request.json())
# request = requests.get(BASE+"posts/e")
# print(request.json())
my_secret = os.environ['secret_key']
app = Flask(__name__)
app.config["SECRET_KEY"] = my_secret
users = Database()
users.print_all()
posts = Database()
socketio = SocketIO(app)
@socketio.on("new_post")
def new_post(data):
  post = data['post']
  posts.newUser(random_code(), post)
  name = data['name']
  request = requests.put(f"https://Quacker-API.theprogrammerking.repl.co/posts/{random_code()}", {"username":name, "text":post})
  print(request.json())
  request = requests.get("https://Quacker-API.theprogrammerking.repl.co/posts/e")
  print(request.json())
  
@app.route('/logout')
def logout():
  resp = make_response(render_template("logout.html"))
  resp.set_cookie("username1", "", expires=0)
  return resp
@app.route('/')
def home():
    username = request.cookies.get("username1")
    if username == None:
      return render_template('home.html') 
    else:
      return redirect(f'/users/{username.lower()}')
@app.route('/signup')
def signup():
    return render_template("signup.html")
@app.route('/confirm', methods=["POST"])
def confirm():
  username, password = request.form["username"], request.form["password"]
  users.newUser(username, password)
  users.print_all()
  request_var = requests.put(f"https://Quacker-API.theprogrammerking.repl.co/posts/{username}")
  resp = make_response(render_template("confirm.html"))
  resp.set_cookie("username1", username)
  return resp
@app.route('/login')
def login():
  return render_template("login.html")
@app.route('/check', methods=["POST"])
def check():
  username, password = request.form["username"], request.form["password"]
  if users.login(username, password):
    resp = make_response(render_template("check.html"))
    resp.set_cookie("user", username)
    return resp
  else:
    return "Invalid Username or Password" 

    
@app.route('/app')
def main_app():
  username = request.cookies.get("username1")
  if username == None:
      return redirect('/')
  else:
    return render_template("index.html", user=username)


@app.route("/users/<user>")
def user(user):
  username = request.cookies.get("username1")
  print(user)
  for item in users.get_all():
    if user == item.lower() and username.lower() ==user:
      return render_template("user_page.html", name=user) 
    elif user == item.lower():
      return "cool"
    else:
      return "this is not a user"
if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0')