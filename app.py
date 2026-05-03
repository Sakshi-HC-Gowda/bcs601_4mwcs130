from flask import Flask, render_template, request
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

# ✅ ADD THIS FUNCTION
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount INTEGER,
        category TEXT,
        date TEXT
    )
    """)
    conn.commit()
    conn.close()

# ✅ CALL IT HERE (important for Render)
init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cursor = conn.cursor()

    # INSERT DATA
    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]

        cursor.execute(
            "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
            (amount, category, date)
        )
        conn.commit()

    # FETCH ALL DATA (ordered by date descending)
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC, id DESC")
    data = cursor.fetchall()

    # TOTAL EXPENSE
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    # TODAY'S TOTAL
    today = datetime.today().strftime('%Y-%m-%d')
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE date = ?", (today,))
    today_total = cursor.fetchone()[0]

    # LAST 7 DAYS TOTAL
    week_ago = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?",
        (week_ago, today)
    )
    week_total = cursor.fetchone()[0]

    # DAILY BREAKDOWN — sum per day for the last 30 days
    cursor.execute(
        """
        SELECT date, SUM(amount) as day_total
        FROM expenses
        WHERE date BETWEEN ? AND ?
        GROUP BY date
        ORDER BY date DESC
        """,
        ((datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d'), today)
    )
    daily_totals = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        expenses=data,
        total=total,
        today_total=today_total,
        week_total=week_total,
        daily_totals=daily_totals
    )

if __name__ == "__main__":
    app.run(debug=True)