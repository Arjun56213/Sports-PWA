from flask import Flask, render_template, request, session, redirect
import db

app = Flask(__name__)
app.secret_key = "sportvault-secret-key"

@app.after_request
def SetSecurityHeaders(response):
    response.headers["Content-Security-Policy"] = "script-src 'self';"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response



@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def Login():
    if session.get("username"):
        return redirect("/home")
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.check_login(username, password)
        if user:
            session["user_id"] = user.user_id
            session["username"] = user.username
            return redirect("/home")
        else:
            error = "Invalid username or password."
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def Register():
    if session.get("username"):
        return redirect("/home")
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        ok, error = db.register_user(username, password)
        if ok:
            return redirect("/login")
    return render_template("register.html", error=error)

@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/login")



@app.route("/home")
def Home():
    if not session.get("username"):
        return redirect("/login")
    return render_template("index.html",
        batting=db.get_all_batting(),
        bowling=db.get_all_bowling(),
        soccer=db.get_all_soccer()
    )

@app.route("/profile")
def Profile():
    if not session.get("username"):
        return redirect("/login")
    user_id = session["user_id"]

    current_user = db.get_user_by_id(user_id)
    return render_template("profile.html",
        user=current_user,
        batting=db.get_batting_by_user(user_id),
        bowling=db.get_bowling_by_user(user_id),
        soccer=db.get_soccer_by_user(user_id),
        batting_stats=db.batting_stats(user_id),
        bowling_stats=db.bowling_stats(user_id),
        soccer_stats=db.soccer_stats(user_id),
        own_profile=True
    )

@app.route("/user/<int:user_id>")
def UserProfile(user_id):
    if not session.get("username"):
        return redirect("/login")
    user = db.get_user_by_id(user_id)
    if not user:
        return redirect("/home")
    return render_template("profile.html",
        user=user,
        batting=db.get_batting_by_user(user_id),
        bowling=db.get_bowling_by_user(user_id),
        soccer=db.get_soccer_by_user(user_id),
        batting_stats=db.batting_stats(user_id),
        bowling_stats=db.bowling_stats(user_id),
        soccer_stats=db.soccer_stats(user_id),
        own_profile=False
    )

@app.route("/search")
def Search():
    if not session.get("username"):
        return redirect("/login")
    query = request.args.get("q", "")
    results = db.search_users(query) if query else []
    return render_template("search.html", results=results, query=query)


@app.route("/delete/<sport>/<int:entry_id>")
def delete_entry_route(sport, entry_id):
    if 'user_id' not in session:
        return redirect("/login")
    
    config = {
        "batting": ("Cricket_Batting", "batting_id"),
        "bowling": ("Cricket_Bowling", "bowling_id"),
        "soccer": ("Soccer_Performance", "match_id")
    }
    
    if sport in config:
        table, id_col = config[sport]
        db.delete_entry(table, id_col, entry_id, session['user_id'])
    
    return redirect("/profile")



@app.route("/add/batting", methods=["GET", "POST"])
def AddBatting():
    if not session.get("username"):
        return redirect("/login")
    if request.method == "POST":
        db.add_batting(session["user_id"], request.form["date"],
            request.form["opposition"], request.form["venue"],
            request.form["format"], int(request.form["runs"]),
            int(request.form["balls"]), request.form["dismissal"])
        return redirect("/profile")
    return render_template("add_batting.html")

@app.route("/edit/batting/<int:batting_id>", methods=["GET", "POST"])
def EditBatting(batting_id):
    if not session.get("username"):
        return redirect("/login")
    entry = db.get_batting_by_id(batting_id)

    if not entry or entry.user_id != session["user_id"]:
        return redirect("/profile")
    if request.method == "POST":
        db.update_batting(batting_id, session["user_id"],
            request.form["date"], request.form["opposition"],
            request.form["venue"], request.form["format"],
            int(request.form["runs"]), int(request.form["balls"]),
            request.form["dismissal"])
        return redirect("/profile")
    return render_template("edit_batting.html", entry=entry)

@app.route("/add/bowling", methods=["GET", "POST"])
def AddBowling():
    if not session.get("username"):
        return redirect("/login")
    if request.method == "POST":
        db.add_bowling(session["user_id"], request.form["date"],
            request.form["opposition"], request.form["venue"],
            request.form["format"], float(request.form["overs"]),
            int(request.form["wickets"]), int(request.form["runs_conceded"]))
        return redirect("/profile")
    return render_template("add_bowling.html")

@app.route("/edit/bowling/<int:bowling_id>", methods=["GET", "POST"])
def EditBowling(bowling_id):
    if not session.get("username"):
        return redirect("/login")
    entry = db.get_bowling_by_id(bowling_id)
    if not entry or entry.user_id != session["user_id"]:
        return redirect("/profile")
    if request.method == "POST":
        db.update_bowling(bowling_id, session["user_id"],
            request.form["date"], request.form["opposition"],
            request.form["venue"], request.form["format"],
            float(request.form["overs"]), int(request.form["wickets"]),
            int(request.form["runs_conceded"]))
        return redirect("/profile")
    return render_template("edit_bowling.html", entry=entry)

@app.route("/add/soccer", methods=["GET", "POST"])
def AddSoccer():
    if not session.get("username"):
        return redirect("/login")
    if request.method == "POST":
        db.add_soccer(session["user_id"], request.form["date"],
            request.form["opposition"], request.form["venue"],
            int(request.form["goals"]), int(request.form["assists"]),
            request.form["result"])
        return redirect("/profile")
    return render_template("add_soccer.html")

@app.route("/edit/soccer/<int:match_id>", methods=["GET", "POST"])
def EditSoccer(match_id):
    if not session.get("username"):
        return redirect("/login")
    entry = db.get_soccer_by_id(match_id)
    if not entry or entry.user_id != session["user_id"]:
        return redirect("/profile")
    if request.method == "POST":
        db.update_soccer(match_id, session["user_id"],
            request.form["date"], request.form["opposition"],
            request.form["venue"], int(request.form["goals"]),
            int(request.form["assists"]), request.form["result"])
        return redirect("/profile")
    return render_template("edit_soccer.html", entry=entry)

if __name__ == "__main__":
    db.InitDB() 
    app.run(debug=True, port=5000)