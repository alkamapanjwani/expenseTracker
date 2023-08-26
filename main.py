from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
# from flask_session import Session

app = Flask(__name__)
app.secret_key = "expense_tracker"

# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# DB_HOST = "localhost"
# DB_NAME = "expense_tracker_db"
# DB_USER = "postgres"
# DB_PASS = "postgres"

DB_HOST = "dpg-cjiee4fjbvhs7394f1kg-a.oregon-postgres.render.com"
DB_NAME = "expense_tracker_db_gmrf"
DB_USER = "expense_tracker_db_gmrf_user"
DB_PASS = "Fh9ewHDtCE3E1WzDWu2CiwQ5U1P4Xr0B"

@app.route("/")
def login():
    if 'userid' in session:
        return redirect(url_for("index"))
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    if 'userid' in session:
        session.pop('userid',None)
        session.pop('username',None)
        flash("User Logged Out")
    return render_template('login.html');


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/home")
def index():
    if 'userid' in session:
        return render_template("index.html",res={"username":session['username']})
    else:
        return redirect(url_for("login"))


@app.route("/login_authorize", methods=["POST"])
def login_authorize():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = validate_login_authorize(username,password)
        if error is None:
            try:
                conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
                cur = conn.cursor()
                cur.execute("SELECT * FROM users where username=%s and password=%s", (username,password),)
                user_id = cur.fetchone()[0]
                cur.close()
                conn.close()
                print(user_id)
                if not user_id:
                    flash("Username or Password is Incorrect")
                    return redirect(url_for("login"))
                else:
                    session['userid'] = user_id
                    # print(session['userid'])
                    session['username'] = request.form.get("username")
                    # print(session['username'])
                    return redirect(url_for("index"))
            except Exception as error:
                print(error)
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("login"))


@app.route("/register_user", methods=["POST"])
def register_user():
    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        password = request.form["password"]
        error = validate_register_user(fullname,username,password)
        if error is None:
            try:
                conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
                cur = conn.cursor()
                cur.execute("INSERT INTO users(full_name, username, password) VALUES (%s, %s, %s)",
                            (fullname,username,password),)
                conn.commit()
                cur.close()
                conn.close()
                flash("User Added Successflly. Please try logging in.")
                return redirect(url_for("login"))

            except Exception as error:
                print(error)
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("register"))


@app.route("/expense_head")
def expense_head():
    if 'userid' in session:
        try:
            conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            cur = conn.cursor()
            cur.execute("SELECT * FROM expense_head where user_id=%s", (session['userid'],) )
            data = cur.fetchall()
            cur.close()
            conn.close()
            return render_template("expense_head.html", res={"username": session['username'],"expense_head":data})
        except Exception as error:
            print(error)
            return render_template("error_occured.html")
    else:
        return redirect(url_for("login"))

@app.route("/insert_expense_head", methods=["POST"])
def insert_expense_head():
    if request.method == "POST":
        name = request.form["name"]
        error = validate_head(name)
        if error is None:
            try:
                conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
                cur = conn.cursor()
                cur.execute("INSERT INTO expense_head(expense_head_name, user_id ) VALUES (%s, %s)",
                            (name,session['userid']),)
                conn.commit()
                cur.close()
                conn.close()
                flash("Data Inserted Successfully")
                return redirect(url_for("expense_head"))
            except Exception as error:
                print(error)
                print(name)
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("expense_head"))


@app.route("/update_expense_head", methods=["POST", "GET"])
def update_expense_head():
    if request.method == "POST":
        id_data = request.form["id"]
        name = request.form["name"]
        error = validate_head(name)
        if error is None:
            try:
                conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
                cur = conn.cursor()
                cur.execute("UPDATE expense_head SET expense_head_name=%s  WHERE expense_head_id=%s",
                    (name, id_data), )
                conn.commit()
                cur.close()
                conn.close()
                flash("Data Updated Successfully")
                return redirect(url_for("expense_head"))
            except Exception as error:
                print(error)
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("expense_head"))


@app.route("/income_head")
def income_head():
    if 'userid' in session:
        try:
            conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            cur = conn.cursor()
            cur.execute("SELECT * FROM income_head where user_id=%s", (session['userid'],) )
            data = cur.fetchall()
            cur.close()
            conn.close()
            return render_template("income_head.html", res={"username": session['username'], "income_head": data})
        except Exception as error:
            print(error)
            return render_template("error_occured.html")
    else:
        return redirect(url_for("login"))

@app.route("/insert_income_head", methods=["POST"])
def insert_income_head():
    if request.method == "POST":
        name = request.form["name"]
        error = validate_head(name)
        if error is None:
            try:
                conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
                cur = conn.cursor()
                cur.execute("INSERT INTO income_head(income_head_name, user_id ) VALUES (%s, %s)",
                            (name,session['userid']),)
                conn.commit()
                cur.close()
                conn.close()
                flash("Data Inserted Successfully")
                return redirect(url_for("income_head"))
            except Exception as error:
                print(error)
                print(name)
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("income_head"))


@app.route("/update_income_head", methods=["POST", "GET"])
def update_income_head():
    if request.method == "POST":
        id_data = request.form["id"]
        name = request.form["name"]
        error = validate_head(name)
        if error is None:
            try:
                conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
                cur = conn.cursor()
                cur.execute("UPDATE income_head SET income_head_name=%s  WHERE income_head_id=%s",
                    (name, id_data), )
                conn.commit()
                cur.close()
                conn.close()
                flash("Data Updated Successfully")
                return redirect(url_for("income_head"))
            except Exception as error:
                print(error)
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("income_head"))


@app.route("/record_expense")
def record_expense():
    if 'userid' in session:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor()
        cur.execute("SELECT * FROM expense_head where user_id=%s", (session['userid'],))
        expense_head_list = cur.fetchall()
        cur.execute("SELECT * FROM income_head where user_id=%s", (session['userid'],))
        income_head_list = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("record_expense.html",res={"username":session['username'],"expense_head_list":expense_head_list,
                                                          "income_head_list":income_head_list})
    else:
        return redirect(url_for("login"))


@app.route("/insert_record_expense", methods=["POST"])
def insert_record_expense():
    if request.method == "POST":
        amount = request.form["amount"]
        comment = request.form["comment"]
        income_head_id = request.form.get('income_head_id')
        expense_head_id = request.form.get('expense_head_id')
        error = validate_insert_record_expense(amount,income_head_id,expense_head_id)
        if error is None:
            try:
                conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
                cur = conn.cursor()
                cur.execute("INSERT INTO expense_list(amount,comment,income_head_id,expense_head_id,user_id ) VALUES (%s,%s,%s,%s,%s)",
                            (amount,comment,income_head_id,expense_head_id,session['userid']),)
                conn.commit()
                cur.close()
                conn.close()
                flash("Expense Recorded Successfully")
                return redirect(url_for("record_expense"))
            except Exception as error:
                print(error)
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("record_expense"))


@app.route("/expense_report", methods=["POST", "GET"])
def expense_report():
    if 'userid' in session:
        try:
            conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            cur = conn.cursor()
            cur.execute("SELECT * FROM expense_head where user_id=%s", (session['userid'],))
            expense_head_list = cur.fetchall()
            cur.close()
            conn.close()
            if request.method == "POST":
                fromdate = request.form["fromdate"]
                todate = request.form["todate"]
                expense_head_id = request.form.get('expense_head_id')
                conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
                cur = conn.cursor()
                cur.execute("SELECT el.expense_list_id,el.created_timestamp,ih.income_head_name,el.comment,el.amount "
                            "FROM expense_list el inner join income_head ih on el.income_head_id = ih.income_head_id "
                            "where el.user_id=%s and el.expense_head_id=%s ORDER BY expense_list_id desc",
                            (session['userid'],expense_head_id))
                trans_list = cur.fetchall()
                print(type(trans_list))
                print(trans_list)
                TotalAmt=sum([pair[4] for pair in trans_list])
                cur.close()
                cur.close()
                conn.close()
                return render_template("expense_report.html",res={"username":session['username'],
                                                                  "expense_head_list":expense_head_list,
                                                                  "expense_head_id":expense_head_id,"trans_list":trans_list,
                                                                  "fromdate":fromdate,
                                                                  "todate":todate,"TotalAmt":TotalAmt})
            else:
                return render_template("expense_report.html",res={"username":session['username'],
                                                                  "expense_head_list":expense_head_list})
        except Exception as error:
            print(error)
            return render_template("error_occured.html")
    else:
        return redirect(url_for("login"))


def validate_login_authorize(username,password):
    error = None
    if not username:
        error = "username is required."
    elif not password:
        error = "password is required."
    print(error)
    return error


def validate_register_user(fullname,username,password):
    error = None
    if not fullname:
        error = "fullname is required."
    elif not username:
        error = "username is required."
    elif not password:
        error = "password is required."
    print(error)
    return error


def validate_head(name):
    error = None
    if not name:
        error = "name is required."
    print(error)
    return error


def validate_insert_record_expense(amount,income_head_id,expense_head_id):
    error = None
    if not amount:
        error = "amount is required."
    elif not income_head_id:
        error = "income head is required."
    elif not expense_head_id:
        error = "expense head is required."
    print(error)
    return error


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
