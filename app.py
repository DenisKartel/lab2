
from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db, init_db

app = Flask(__name__)
app.secret_key = "lab2_secret_key_for_testing"


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()

        try:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            db.commit()
            db.close()

            return redirect(url_for("login"))

        except Exception:
            db.close()
            return render_template(
                "message.html",
                title="Ошибка регистрации",
                text="Username already exists or registration error",
                back_url="/register",
                back_label="Попробовать снова"
            )

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()

        # INTENTIONALLY VULNERABLE: SQL Injection
        query = (
            f"SELECT * FROM users "
            f"WHERE username = '{username}' "
            f"AND password = '{password}'"
        )

        user = db.execute(query).fetchone()
        db.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))

        return render_template(
            "message.html",
            title="Ошибка входа",
            text="Invalid username or password",
            back_url="/login",
            back_label="Попробовать снова"
        )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"],
        user_id=session["user_id"]
    )


@app.route("/profile/<int:user_id>")
def profile(user_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()

    # INTENTIONALLY VULNERABLE:
    # No check that the requested profile belongs to the current user.
    user = db.execute(
        "SELECT id, username FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    db.close()

    if not user:
        return render_template(
            "message.html",
            title="Не найдено",
            text="User not found",
            back_url="/dashboard",
            back_label="В кабинет"
        ), 404

    return render_template("profile.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
