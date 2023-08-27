from db_connect import DB

class expense_head:
    def expense_head(self,userid):
        dbObj = DB()
        dets = dbObj.execute_fetchall("SELECT * FROM expense_head where user_id=%s", (userid,) )
        dbObj.destroy()
        return dets

    def insert_expense_head(self,name,userid):
        dbObj = DB()
        dbObj.execute("INSERT INTO expense_head(expense_head_name, user_id ) VALUES (%s, %s)",
                            (name,userid),)
        dbObj.destroy()


    def update_expense_head(self,name,id_data):
        dbObj = DB()
        dbObj.execute("UPDATE expense_head SET expense_head_name=%s  WHERE expense_head_id=%s",
                    (name, id_data), )
        dbObj.destroy()
