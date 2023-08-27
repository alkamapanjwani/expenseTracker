from db_connect import DB

class record_expense:
    def insert_record_expense(self,fromdate,amount,comment,income_head_id,expense_head_id,userid):
        dbObj = DB()
        dbObj.execute("INSERT INTO expense_list(created_timestamp,amount,comment,income_head_id,expense_head_id,user_id ) VALUES (%s,%s,%s,%s,%s,%s)",
                            (fromdate,amount,comment,income_head_id,expense_head_id,userid),)
        dbObj.destroy()

