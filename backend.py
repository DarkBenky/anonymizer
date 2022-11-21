import sqlite3 as sql
import hashlib
import string
import random
import streamlit as st

st.set_page_config(layout="wide")

if "page" not in st.session_state:
	st.session_state.page = "login"
if "user" not in st.session_state:
	st.session_state.user = "user"

def hash_password(password):
	return hashlib.sha256(password.encode()).hexdigest()

def hash_password_short(password):
	return hashlib.sha1(password.encode()).hexdigest()

def salt_password(password):
	salt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
	return hash_password(salt + password) , salt

def pepper_password(password):
	return hash_password(password + "i am a peper")

def chilli_password(password):
	new_hash = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
	new_hash = hash_password(new_hash)
	return password + new_hash[:32] , new_hash

def un_chilli_password(password,chilli):
	return password + chilli[:32]

def shuffle(array : list):
	seq = [i for i in range(len(array))]
	random.shuffle(seq)
	# shuffle chunks
	for i in range(len(seq)):
		array[i] , array[seq[i]] = array[seq[i]] , array[i]
	return array , seq

def un_shuffle(password : str , seq : str):
	seq = [int(i) for i in seq.split("-")]
	chunk = len(password) // len(seq)
	password_chunks = [password[i:i+chunk] for i in range(0, len(password), chunk)]
	for i in range(len(seq)):
		password_chunks[i] , password_chunks[seq[i]] = password_chunks[seq[i]] , password_chunks[i]
	return ''.join(password_chunks)
	
def cook_password(password):
	# split password into chunks with same length
	while True:
		chunk = random.randint(2,len(password))
		if len(password) % chunk == 0:
			break
	password_chunks = [password[i:i+chunk] for i in range(0, len(password), chunk)]
	# shuffle chunks
	password_chunks , seq = shuffle(password_chunks)
	return ''.join(password_chunks) , "-".join([str(i) for i in seq])


class Database():
	def __init__(self):
		self.db = sql.connect("user_login.db")
		self.cursor = self.db.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT , salt TEXT , chilli TEXT , seq TEXT , type_of_account TEXT)")
		self.db.commit()
	def add_user(self,username : str , password : str , type_of_account : str):
		password = pepper_password(password)
		password , chilli =  chilli_password(password)
		password = hash_password_short(password)
		password , salt = salt_password(password)
		password , seq = cook_password(password)
		self.cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?)",(username,password,salt,chilli,seq,type_of_account))
		self.db.commit()
	def get_user(self,username : str ):
		self.cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
		user = self.cursor.fetchone()
		if user is None:
			return None
		return user
	def login_user(self,username : str , password : str):
		self.cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
		user = self.cursor.fetchone()
		if user is None:
			return None
		password = pepper_password(password)
		password = un_chilli_password(password,user[3])
		password = hash_password_short(password)
		password = hash_password(user[2] + password)
		password = un_shuffle(password,user[4])
		if password == user[1]:
			return user
		return False
	def edit_user(self,username : str , password : str , new_password : str):
		self.cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
		user = self.cursor.fetchone()
		if user is None:
			return None
		password = pepper_password(password)
		password = un_chilli_password(password,user[3])
		password = hash_password_short(password)
		password = hash_password(user[2] + password)
		password = un_shuffle(password,user[4])
		if password == user[1]:
			password , salt = salt_password(pepper_password(new_password))
			password = hash_password(password)
			self.cursor.execute("UPDATE users SET password = ? , salt = ? WHERE username = ?",(password,salt,username))
			self.db.commit()
			return True
		return False
	def delete_user(self,username : str , password : str):
		self.cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
		user = self.cursor.fetchone()
		if user is None:
			return None
		password = pepper_password(password)
		password = hash_password(password)
		password = hash_password(user[2] + (password))
		if password == user[1]:
			self.cursor.execute("DELETE FROM users WHERE username = ?",(username,))
			self.db.commit()
			return True
		return False
	def get_all_users(self):
		self.cursor.execute("SELECT * FROM users")
		users = self.cursor.fetchall()
		return users

database = Database()

def login():
	st.title("Login")
	username = st.text_input("Username")
	password = st.text_input("Password",type="password")
	if st.button("Login"):
		user = database.login_user(username,password)
		if user is None:
			st.error("Invalid username or password")
		else:
			st.success("Logged in")
			st.session_state.page = "home"
			st.session_state.user = user
			st.experimental_rerun()
	if st.button("Go to Register"):
		st.session_state.page = "register"
		st.experimental_rerun()

def register():
	st.title("Register")
	username = st.text_input("Username")
	password = st.text_input("Password",type="password")
	user_type = st.selectbox("User Type",["user","admin"])
	if st.button("Register"):
		user = database.get_user(username)
		if user is not None:
			st.error("User already exists")
		else:
			database.add_user(username,password,user_type)
			st.success("User created successfully")
	if st.button("Go to Login"):
		st.session_state.page = "login"
		st.experimental_rerun()
			
def home():
	c1 , c2 , c3 , c4 , c5 , c6 = st.columns(6)
	with c6:
		st.write(st.session_state.user)
	st.title("Home Page")
	if st.session_state.user[5] == "admin":
		if st.button("Go to Admin"):
			st.session_state.page = "admin"
			st.experimental_rerun()
	if st.button("Anonymizer"):
		st.session_state.page = "anonymizer"
		st.experimental_rerun()
	if st.button("Logout"):
		st.session_state.page = "login"
		st.experimental_rerun()

def admin():
	c1 , c2 , c3 , c4 , c5 , c6 = st.columns(6)
	with c6:
		st.write(st.session_state.user)
	st.title("Admin Page")
	users = database.get_all_users()
	st.write(users)
	if st.button("Go to Home"):
		st.session_state.page = "home"
		st.experimental_rerun()
	if st.button("Logout"):
		st.session_state.page = "login"
		st.experimental_rerun()

def anonymizer():
	st.title("Anonymizer")
	upload_file = st.sidebar.file_uploader("Upload a file")
	if upload_file is not None:
		pass
	if st.button("Go to Home"):
		st.session_state.page = "home"
		st.experimental_rerun()
	


if st.session_state.page == "login":
	login()
elif st.session_state.page == "register":
	register()
elif st.session_state.page == "home":
	home()
elif st.session_state.page == "admin":
	admin()
elif st.session_state.page == "anonymizer":
	anonymizer()

		




