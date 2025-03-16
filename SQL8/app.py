from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Fungsi untuk menghubungkan ke database
def get_db_connection():
    conn = sqlite3.connect('appointments.db')
    conn.row_factory = sqlite3.Row  
    return conn

# Inisialisasi database
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            patient_email TEXT NOT NULL,
            doctor_name TEXT NOT NULL,
            doctor_email TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            complaint TEXT NOT NULL
        )
    ''')
    conn.close()

# Route halaman utama
@app.route('/')
def index():
    conn = get_db_connection()
    appointments = conn.execute('SELECT * FROM appointments').fetchall()
    conn.close()
    return render_template('index.html', appointments=appointments)

# Route untuk menambah tiket
@app.route('/add', methods=['POST'])
def add():
    pname = request.form['patient_name']
    pemail = request.form['patient_email']
    dname = request.form['doctor_name']
    demail = request.form['doctor_email']
    appointment_date = request.form['appointment_date']
    complaint = request.form['complaint']

    if pname and pemail and dname and demail and appointment_date and complaint:
        conn = get_db_connection()
        conn.execute('INSERT INTO appointments (patient_name, patient_email, doctor_name, doctor_email, appointment_date, complaint) VALUES (?, ?, ?, ?, ?, ?)',
                     (pname, pemail, dname, demail, appointment_date, complaint))
        conn.commit()
        conn.close()
    
    return redirect(url_for('index'))

# Route untuk menghapus tiket
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM appointments WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
