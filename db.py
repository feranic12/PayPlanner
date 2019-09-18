import sqlite3


class DB:

    def __init__(self):
        self.con = sqlite3.connect("pay_planner_db.db")

    def get_all_rows(self):
        cur = self.con.cursor()
        sql = "select * from tbl"
        try:
            cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print("Ошибка")
        else:
            print ("Успех")
            result = cur.fetchone()
            self.con.commit()
            cur.close()
            return result

    def quit(self):
        self.con.close()