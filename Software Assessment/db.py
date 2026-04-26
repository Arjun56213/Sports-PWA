import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


DB_FOLDER = "database" 
DB_PATH = os.path.join(DB_FOLDER, "sportvault.db")

#User Class - represents a user in the system

class User:
    def __init__(self, user_id, username, created_at):
        self.user_id = user_id
        self.username = username
        self.created_at = created_at

#Batting Class - represents a batting performance entry

class BattingPerformance:
    def __init__(self, performance_id, user_id, date, opposition, venue, format, runs, balls, dismissal, username=None):
        self.batting_id = performance_id
        self.user_id = user_id
        self.date = date
        self.opposition = opposition
        self.venue = venue
        self.format = format
        self.runs = runs
        self.balls = balls
        self.dismissal = dismissal
        self.username = username 

#Bowling Class - represents a bowling performance entry

class BowlingPerformance:
    def __init__(self, bowling_id, user_id, date, opposition, venue, format, overs, wickets, runs_conceded, username=None):
        self.bowling_id = bowling_id
        self.user_id = user_id
        self.date = date
        self.opposition = opposition
        self.venue = venue
        self.format = format
        self.overs = overs
        self.wickets = wickets
        self.runs_conceded = runs_conceded
        self.username = username

#Soccer Class - represents a soccer performance entry

class SoccerPerformance:
    def __init__(self, match_id, user_id, date, opposition, venue, goals, assists, result, username=None):
        self.match_id = match_id
        self.user_id = user_id
        self.date = date
        self.opposition = opposition
        self.venue = venue
        self.goals = goals
        self.assists = assists
        self.result = result
        self.username = username

# --- DATABASE FUNCTIONS ---

def GetDB():
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db

def InitDB():
    db = GetDB()
    base_path = os.path.dirname(__file__)
    sql_path = os.path.join(base_path, DB_FOLDER, 'queries.sql')
    with open(sql_path, 'r') as f:
        db.executescript(f.read())
    db.commit()
    db.close()

#Registration Functions - checks if username is taken and hashes password before storing in database

def register_user(username, password):
    if not username or not password:
        return False, "Username and password required."
    p_hash = generate_password_hash(password)
    created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = GetDB()
    try:
        db.execute("INSERT INTO Users (username, password_hash, salt, created_at) VALUES (?, ?, ?, ?)",
                  (username, p_hash, "na", created))
        db.commit()
        return True, None
    except sqlite3.IntegrityError:
        return False, "Username already taken."
    finally:
        db.close()

#Login Functions - checks if username exists and password matches

def check_login(username, password):
    db = GetDB()
    row = db.execute("SELECT * FROM Users WHERE username = ?", (username,)).fetchone()
    db.close()
    if row and check_password_hash(row["password_hash"], password):
        return User(row["user_id"], row["username"], row["created_at"])
    return None

def get_user_by_id(user_id):
    db = GetDB()
    row = db.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,)).fetchone()
    db.close()
    if row:
        return User(row["user_id"], row["username"], row["created_at"])
    return None

# Functions for adding, retrieving, updating, and deleting performance entries for batting, bowling, and soccer

def add_batting(user_id, date, opposition, venue, format, runs, balls, dismissal):
    db = GetDB()
    db.execute('''INSERT INTO Cricket_Batting (user_id, date, opposition, venue, format, runs, balls, dismissal) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
               (user_id, date, opposition, venue, format, runs, balls, dismissal))
    db.commit()
    db.close()



def get_all_batting():
    db = GetDB()

    rows = db.execute("SELECT Cricket_Batting.*, Users.username FROM Cricket_Batting JOIN Users ON Cricket_Batting.user_id = Users.user_id ORDER BY date DESC").fetchall()
    db.close()

    return [BattingPerformance(r["batting_id"], r["user_id"], r["date"], r["opposition"], r["venue"], r["format"], r["runs"], r["balls"], r["dismissal"], r["username"]) for r in rows]

def get_batting_by_user(user_id):
    db = GetDB()
    rows = db.execute("SELECT * FROM Cricket_Batting WHERE user_id = ? ORDER BY date DESC", (user_id,)).fetchall()
    db.close()

    return [BattingPerformance(r["batting_id"], r["user_id"], r["date"], r["opposition"], r["venue"], r["format"], r["runs"], r["balls"], r["dismissal"]) for r in rows]

def get_batting_by_id(performance_id):
    db = GetDB()

    r = db.execute("SELECT * FROM Cricket_Batting WHERE batting_id = ?", (performance_id,)).fetchone()
    db.close()
    return BattingPerformance(r["batting_id"], r["user_id"], r["date"], r["opposition"], r["venue"], r["format"], r["runs"], r["balls"], r["dismissal"]) if r else None


def add_bowling(user_id, date, opposition, venue, format, overs, wickets, runs_conceded):
    db = GetDB()
    db.execute('''INSERT INTO Cricket_Bowling (user_id, date, opposition, venue, format, overs, wickets, runs_conceded) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
               (user_id, date, opposition, venue, format, overs, wickets, runs_conceded))
    db.commit()
    db.close()

def get_all_bowling():
    db = GetDB()
    rows = db.execute("SELECT Cricket_Bowling.*, Users.username FROM Cricket_Bowling JOIN Users ON Cricket_Bowling.user_id = Users.user_id ORDER BY date DESC").fetchall()
    db.close()
    return [BowlingPerformance(r["bowling_id"], r["user_id"], r["date"], r["opposition"], r["venue"], r["format"], r["overs"], r["wickets"], r["runs_conceded"], r["username"]) for r in rows]

def get_bowling_by_user(user_id):
    db = GetDB()
    rows = db.execute("SELECT * FROM Cricket_Bowling WHERE user_id = ? ORDER BY date DESC", (user_id,)).fetchall()
    db.close()
    return [BowlingPerformance(r["BOWLING_ID"], r["USER_ID"], r["DATE"], r["OPPOSITION"], r["VENUE"], r["FORMAT"], r["OVERS"], r["WICKETS"], r["RUNS_CONCEDED"]) for r in rows]
def get_bowling_by_id(bowling_id):
    db = GetDB()
    r = db.execute("SELECT * FROM Cricket_Bowling WHERE bowling_id = ?", (bowling_id,)).fetchone()
    db.close()
    return BowlingPerformance(r["bowling_id"], r["user_id"], r["date"], r["opposition"], r["venue"], r["format"], r["overs"], r["wickets"], r["runs_conceded"]) if r else None



def add_soccer(user_id, date, opposition, venue, goals, assists, result):
    db = GetDB()
    db.execute("INSERT INTO Soccer_Performance (user_id, date, opposition, venue, goals, assists, result) VALUES (?, ?, ?, ?, ?, ?, ?)",
               (user_id, date, opposition, venue, goals, assists, result))
    db.commit()
    db.close()

def get_all_soccer():
    db = GetDB()
    rows = db.execute("SELECT Soccer_Performance.*, Users.username FROM Soccer_Performance JOIN Users ON Soccer_Performance.user_id = Users.user_id ORDER BY date DESC").fetchall()
    db.close()
    return [SoccerPerformance(r["match_id"], r["user_id"], r["date"], r["opposition"], r["venue"], r["goals"], r["assists"], r["result"], r["username"]) for r in rows]

def get_soccer_by_user(user_id):
    db = GetDB()
    rows = db.execute("SELECT * FROM Soccer_Performance WHERE user_id = ? ORDER BY date DESC", (user_id,)).fetchall()
    db.close()
    return [SoccerPerformance(r["MATCH_ID"], r["USER_ID"], r["DATE"], r["OPPOSITION"], r["VENUE"], r["GOALS"], r["ASSISTS"], r["RESULT"]) for r in rows]
def get_soccer_by_id(match_id):
    db = GetDB()
    r = db.execute("SELECT * FROM Soccer_Performance WHERE match_id = ?", (match_id,)).fetchone()
    db.close()
    return SoccerPerformance(r["match_id"], r["user_id"], r["date"], r["opposition"], r["venue"], r["goals"], r["assists"], r["result"]) if r else None



def delete_entry(table_name, id_column, entry_id, user_id):
    db = GetDB()
    db.execute(f"DELETE FROM {table_name} WHERE {id_column} = ? AND user_id = ?", (entry_id, user_id))
    db.commit()
    db.close()

# Search function for users based on username query

def search_users(query):
    db = GetDB()
    rows = db.execute("SELECT * FROM Users WHERE username LIKE ?", (f"%{query}%",)).fetchall()
    db.close()
    return [User(r["user_id"], r["username"], r["created_at"]) for r in rows]

# Functions to calculate statistics for batting, bowling, and soccer performances for a given user

def batting_stats(user_id):
    db = GetDB()
    row = db.execute('''
        SELECT 
            SUM(runs) as total_runs, 
            MAX(runs) as high_score,
            AVG(runs) as batting_avg
        FROM Cricket_Batting 
        WHERE user_id = ?
    ''', (user_id,)).fetchone()
    db.close()

    if row and row["total_runs"] is not None:
        return {
            "total_runs": row["total_runs"],
            "high_score": row["high_score"],
            "batting_avg": round(row["batting_avg"], 2)
        }
    return {"total_runs": 0, "high_score": 0, "batting_avg": 0}

def bowling_stats(user_id):
    db = GetDB()
    row = db.execute('''
        SELECT 
            COUNT(*) as matches,
            SUM(wickets) as total_wickets,
            AVG(wickets) as bowling_avg,
            SUM(runs_conceded) as total_runs,
            SUM(overs) as total_overs
        FROM Cricket_Bowling 
        WHERE user_id = ?
    ''', (user_id,)).fetchone()
    db.close()

    if row and row["matches"] > 0:
        # Avoid division by zero for economy
        eco = (row["total_runs"] / row["total_overs"]) if row["total_overs"] and row["total_overs"] > 0 else 0
        return {
            "matches": row["matches"],
            "total_wickets": row["total_wickets"] or 0,
            "bowling_avg": round(row["total_runs"] / row["total_wickets"], 2) if row["total_wickets"] and row["total_wickets"] > 0 else 0,
            "economy": round(eco, 2)
        }
    return {"matches": 0, "total_wickets": 0, "bowling_avg": 0, "economy": 0}

def soccer_stats(user_id):
    db = GetDB()
    # Basic totals
    totals = db.execute('''
        SELECT 
            COUNT(*) as matches,
            SUM(goals) as total_goals,
            SUM(assists) as total_assists
        FROM Soccer_Performance 
        WHERE user_id = ?
    ''', (user_id,)).fetchone()

    # Result counts
    wins = db.execute("SELECT COUNT(*) FROM Soccer_Performance WHERE user_id = ? AND result = 'Win'", (user_id,)).fetchone()[0]
    draws = db.execute("SELECT COUNT(*) FROM Soccer_Performance WHERE user_id = ? AND result = 'Draw'", (user_id,)).fetchone()[0]
    losses = db.execute("SELECT COUNT(*) FROM Soccer_Performance WHERE user_id = ? AND result = 'Loss'", (user_id,)).fetchone()[0]
    
    db.close()

    if totals and totals["matches"] > 0:
        return {
            "matches": totals["matches"],
            "total_goals": totals["total_goals"] or 0,
            "total_assists": totals["total_assists"] or 0,
            "wins": wins,
            "draws": draws,
            "losses": losses
        }
    return {"matches": 0, "total_goals": 0, "total_assists": 0, "wins": 0, "draws": 0, "losses": 0}

# Update functions for editing existing entries - checks if entry belongs to user before allowing update

def update_batting(batting_id, user_id, date, opposition, venue, format, runs, balls, dismissal):
    db = GetDB()
    db.execute('''UPDATE Cricket_Batting SET date=?, opposition=?, venue=?, format=?, runs=?, balls=?, dismissal=?
                  WHERE batting_id=? AND user_id=?''',
               (date, opposition, venue, format, runs, balls, dismissal, batting_id, user_id))
    db.commit()
    db.close()

def update_bowling(bowling_id, user_id, date, opposition, venue, format, overs, wickets, runs_conceded):
    db = GetDB()
    db.execute('''UPDATE Cricket_Bowling SET date=?, opposition=?, venue=?, format=?, overs=?, wickets=?, runs_conceded=?
                  WHERE bowling_id=? AND user_id=?''',
               (date, opposition, venue, format, overs, wickets, runs_conceded, bowling_id, user_id))
    db.commit()
    db.close()

def update_soccer(match_id, user_id, date, opposition, venue, goals, assists, result):
    db = GetDB()
    db.execute('''UPDATE Soccer_Performance SET date=?, opposition=?, venue=?, goals=?, assists=?, result=?
                  WHERE match_id=? AND user_id=?''',
               (date, opposition, venue, goals, assists, result, match_id, user_id))
    db.commit()
    db.close()