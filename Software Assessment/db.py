import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB = "database/sportvault.db"

class User:
    def __init__(self, id, username):
        self.user_id = id
        self.username = username

def GetDB():
    return sqlite3.connect(DB)

def InitDB():
    db = GetDB()
    f = open("database/queries.sql")
    db.executescript(f.read())
    db.commit()
    db.close()

def register_user(u, p):
    db = GetDB()
    try:
        db.execute("INSERT INTO Users (username, password_hash) VALUES (?,?)",
                   (u, generate_password_hash(p)))
        db.commit()
        return True, None
    except:
        return False, "error"

def check_login(u, p):
    db = GetDB()
    r = db.execute("SELECT * FROM Users WHERE username=?", (u,)).fetchone()
    db.close()
    if r and check_password_hash(r[2], p):
        return User(r[0], r[1])
    return None

def add_batting(uid, d, o, v, f, r, b, dis):
    db = GetDB()
    db.execute("INSERT INTO Cricket_Batting VALUES (NULL,?,?,?,?,?,?,?,?)",
               (uid, d, o, v, f, r, b, dis))
    db.commit()
    db.close()

def get_all_batting():
    db = GetDB()
    rows = db.execute("SELECT * FROM Cricket_Batting").fetchall()
    db.close()
    return rows

def get_batting_by_user(uid):
    db = GetDB()
    rows = db.execute("SELECT * FROM Cricket_Batting WHERE user_id=?", (uid,)).fetchall()
    db.close()
    return rows

def add_bowling(uid, d, o, v, f, ov, w, r):
    db = GetDB()
    db.execute("INSERT INTO Cricket_Bowling VALUES (NULL,?,?,?,?,?,?,?,?)",
               (uid, d, o, v, f, ov, w, r))
    db.commit()
    db.close()

def get_all_bowling():
    db = GetDB()
    rows = db.execute("SELECT * FROM Cricket_Bowling").fetchall()
    db.close()
    return rows

def get_bowling_by_user(uid):
    db = GetDB()
    rows = db.execute("SELECT * FROM Cricket_Bowling WHERE user_id=?", (uid,)).fetchall()
    db.close()
    return rows

def add_soccer(uid, d, o, v, g, a, r):
    db = GetDB()
    db.execute("INSERT INTO Soccer_Performance VALUES (NULL,?,?,?,?,?,?,?)",
               (uid, d, o, v, g, a, r))
    db.commit()
    db.close()

def get_all_soccer():
    db = GetDB()
    rows = db.execute("SELECT * FROM Soccer_Performance").fetchall()
    db.close()
    return rows

def get_soccer_by_user(uid):
    db = GetDB()
    rows = db.execute("SELECT * FROM Soccer_Performance WHERE user_id=?", (uid,)).fetchall()
    db.close()
    return rows

def search_users(q):
    db = GetDB()
    rows = db.execute("SELECT * FROM Users WHERE username LIKE ?", ("%"+q+"%",)).fetchall()
    db.close()
    return rows