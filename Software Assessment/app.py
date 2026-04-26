from flask import Flask, render_template, request, session, redirect
import db

app = Flask(__name__)



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
            error = "Invalid login"

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def Register():
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

    return render_template("profile.html",
        batting=db.get_batting_by_user(user_id),
        bowling=db.get_bowling_by_user(user_id),
        soccer=db.get_soccer_by_user(user_id)
    )


@app.route("/search")
def Search():
    if not session.get("username"):
        return redirect("/login")

    query = request.args.get("q", "")
    results = db.search_users(query)

    return render_template("search.html", results=results)


@app.route("/add/batting", methods=["GET", "POST"])
def AddBatting():
    if not session.get("username"):
        return redirect("/login")

    if request.method == "POST":
        db.add_batting(
            session["user_id"],
            request.form["date"],
            request.form["opposition"],
            request.form["venue"],
            request.form["format"],
            int(request.form["runs"]),
            int(request.form["balls"]),
            request.form["dismissal"]
        )
        return redirect("/profile")

    return render_template("add_batting.html")


@app.route("/add/bowling", methods=["GET", "POST"])
def AddBowling():
    if not session.get("username"):
        return redirect("/login")

    if request.method == "POST":
        db.add_bowling(
            session["user_id"],
            request.form["date"],
            request.form["opposition"],
            request.form["venue"],
            request.form["format"],
            float(request.form["overs"]),
            int(request.form["wickets"]),
            int(request.form["runs_conceded"])
        )
        return redirect("/profile")

    return render_template("add_bowling.html")


@app.route("/add/soccer", methods=["GET", "POST"])
def AddSoccer():
    if not session.get("username"):
        return redirect("/login")

    if request.method == "POST":
        db.add_soccer(
            session["user_id"],
            request.form["date"],
            request.form["opposition"],
            request.form["venue"],
            int(request.form["goals"]),
            int(request.form["assists"]),
            request.form["result"]
        )
        return redirect("/profile")

    return render_template("add_soccer.html")


if __name__ == "__main__":
    db.InitDB()
    app.run(debug=True)