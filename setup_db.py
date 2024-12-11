
import sqlite3
#create connection to the sqllite database
def create_connection():
    con=sqlite3.connect('budegt_app.db')
    return con
#create user_table
def create_user_table():
    con=create_connection()
    c=con.cursor()
    c.execute(''' create table if not exists user_table(
        id integer primary key autoincrement,username text not null unique,password text not null)''')
    con.commit()
    con.close()
    #create newuser in interface
def create_user(username,password):
    con=create_connection()
    c=con.cursor()
    c.execute("INSERT INTO user_table (username,password) VALUES (?,?)",(username,password))
    con.commit()
    con.close()
def authenticate_user(username,password):
    con=create_connection()
    c=con.cursor()
    c.execute("SELECT * FROM user_table WHERE username=? AND password=?", (username,password))
    user=c.fetchone()
    con.close()
    return user
def create_categories_table():
    con = create_connection()
    c = con.cursor()
    c.execute('''create table if not exists categories_table(
             id integer primary key autoincrement,
              user_id integer,category_name text not null,category_type text not null check(category_type in('expense','income','savings')),foreign key(user_id)references user_table(id)
               )''')
    con.commit()
    con.close()


create_connection()
# create_user_table()
create_categories_table()
# print(authenticate_user('bghjk',3256))
# authenticate_user('ram',3256)
# create_user('ram',3256)
    

