from db_connect import DB
class users:
    def login_authorize(self,username, password):
        dbObj = DB()
        user_dets = dbObj.execute_fetchone("SELECT * FROM users where username=%s and password=%s",
                                         (username, password), )
        dbObj.destroy()
        return user_dets[0],user_dets[2]


    def register_user(self,fullname,username, password):
        dbObj = DB()
        dbObj.execute("INSERT INTO users(full_name, username, password) VALUES (%s, %s, %s)",
                            (fullname,username,password),)
        dbObj.destroy()
