from db_connect import DB

class expense_report:
    def expense_report(self,userid,expense_head_id,fromdate,todate):
        dbObj = DB()
        dets = dbObj.execute_fetchall("SELECT el.expense_list_id,el.created_timestamp,ih.income_head_name,el.comment,el.amount "
                            "FROM expense_list el inner join income_head ih on el.income_head_id = ih.income_head_id "
                            "where el.user_id=%s and el.expense_head_id=%s and date(el.created_timestamp) >= %s "
                            "and date(el.created_timestamp) <= %s ORDER BY expense_list_id desc",
                            (userid,expense_head_id,fromdate,todate))
        dbObj.destroy()
        return dets
