
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'crm.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS klanten (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    naam TEXT,
                    adres TEXT,
                    telefoon TEXT,
                    email TEXT,
                    werkzaamheden TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS contactmomenten (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    klant_id INTEGER,
                    datum TEXT,
                    notitie TEXT,
                    FOREIGN KEY (klant_id) REFERENCES klanten(id)
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def klanten():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM klanten")
    klanten = c.fetchall()
    conn.close()
    return render_template('klanten.html', klanten=klanten)

@app.route('/klant/nieuw', methods=['GET', 'POST'])
def nieuwe_klant():
    if request.method == 'POST':
        data = (
            request.form['naam'],
            request.form['adres'],
            request.form['telefoon'],
            request.form['email'],
            request.form['werkzaamheden']
        )
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO klanten (naam, adres, telefoon, email, werkzaamheden) VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()
        return redirect(url_for('klanten'))
    return render_template('nieuwe_klant.html')

@app.route('/klant/<int:klant_id>')
def klant_detail(klant_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM klanten WHERE id = ?", (klant_id,))
    klant = c.fetchone()
    c.execute("SELECT * FROM contactmomenten WHERE klant_id = ?", (klant_id,))
    contactmomenten = c.fetchall()
    conn.close()
    return render_template('klant_detail.html', klant=klant, contactmomenten=contactmomenten)

@app.route('/klant/<int:klant_id>/contactmoment', methods=['GET', 'POST'])
def nieuw_contactmoment(klant_id):
    if request.method == 'POST':
        data = (
            klant_id,
            request.form['datum'],
            request.form['notitie']
        )
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO contactmomenten (klant_id, datum, notitie) VALUES (?, ?, ?)", data)
        conn.commit()
        conn.close()
        return redirect(url_for('klant_detail', klant_id=klant_id))
    return render_template('nieuw_contactmoment.html', klant_id=klant_id)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
