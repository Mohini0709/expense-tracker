from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = c.fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = request.form['amount']
        description = request.form['description']

        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                  (date, category, amount, description))
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('add_expense.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
