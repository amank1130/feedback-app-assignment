from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

# database file path
DB_FILE = os.environ.get("DB_PATH", "data/feedback.db")


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # make sure data folder exists
    folder = os.path.dirname(DB_FILE)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        # basic validation
        if not name:
            flash("Please enter your name", "error")
            return render_template("form.html", name=name, email=email, message=message)
        if not email or "@" not in email:
            flash("Please enter a valid email", "error")
            return render_template("form.html", name=name, email=email, message=message)
        if not message:
            flash("Please enter a message", "error")
            return render_template("form.html", name=name, email=email, message=message)

        # save to db
        conn = get_db()
        conn.execute(
            "INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )
        conn.commit()
        conn.close()

        flash("Thanks! Your feedback has been submitted.", "success")
        return redirect(url_for("submissions"))

    return render_template("form.html")


@app.route("/submissions")
def submissions():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM feedback ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("submissions.html", rows=rows)


@app.route("/health")
def health():
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
