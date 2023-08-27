from db_connect import DB

class income_head:
    def income_head(self,userid):
        dbObj = DB()
        dets = dbObj.execute_fetchall("SELECT * FROM income_head where user_id=%s", (userid,) )
        dbObj.destroy()
        return dets

    def insert_income_head(self,name,userid):
        dbObj = DB()
        dbObj.execute("INSERT INTO income_head(income_head_name, user_id ) VALUES (%s, %s)",
                            (name,userid),)
        dbObj.destroy()


    def update_income_head(self,name,id_data):
        dbObj = DB()
        dbObj.execute("UPDATE income_head SET income_head_name=%s  WHERE income_head_id=%s",
                    (name, id_data), )
        dbObj.destroy()
