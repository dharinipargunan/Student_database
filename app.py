from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "dharini_pargunan"

DB_HOST = "localhost"
DB_NAME = "Student Database"
DB_USER = "postgres"
DB_PASS = "Dharini"

conn = psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST)

@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM Students"
    cur.execute(s)
    list_users = cur.fetchall()
    return render_template('index.html',list_users=list_users)

@app.route('/add_student',methods=['POST'])
def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        cur.execute("INSERT INTO Students (fname,lname,email) VALUES (%s,%s,%s)", (fname,lname,email))
        conn.commit()
        flash('Student Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>',methods=['POST','GET'])
def get_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Students WHERE stud_id = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    student = data[0]
    return render_template('edit.html', student=student)

@app.route('/update/<id>',methods=['POST'])
def update_student(id):
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE Students
            SET fname = %s,
                lname = %s,
                email = %s
            WHERE stud_id = %s
        """, (fname, lname, email, id))
        flash('Student Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>',methods=['POST','GET'])
def delete_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM Students WHERE stud_id ={0}'.format(id))
    conn.commit()
    flash('Student Record deleted Successfully')
    return redirect(url_for('Index'))


if __name__=="__main__":
    app.run(debug=True)