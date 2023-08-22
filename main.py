from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2


app = Flask(__name__)
app.secret_key = "expense_tracker"


DB_HOST = "localhost"
DB_NAME = "expense_tracker_db"
DB_USER = "postgres"
DB_PASS = "postgres"


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/login_authorize", methods=["POST"])
def login_authorize():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = validate_login_authorize(username,password)
        if error is None:
            try:
                conn = psycopg2.connect(database=DB_NAME,
                                        user=DB_USER,
                                        password=DB_PASS,
                                        host=DB_HOST)
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM users where username=%s and password=%s", (username,password),)
                user_cnt = cur.fetchone()[0]
                cur.close()
                conn.close()
                if user_cnt == 1:
                    print("success")
                    return redirect(url_for("index"))
                else:
                    print("fail")
                    flash("Username or Password is Incorrect")
                    return redirect(url_for("login"))
            except Exception as error:
                print(error)
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("login"))


regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

def validate_login_authorize(username,password):
    error = None
    if not username:
        error = "username is required."
    elif not password:
        error = "password is required."
    print(error)
    return error

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
