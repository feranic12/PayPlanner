import sqlite3


class DB:

    def __init__(self):
        self.con = sqlite3.connect("pay_planner_db.db")

    def get_all_rows(self):
        cur = self.con.cursor()
        sql = """select s.service_name, st.name,bc.bank,bc.number,s.term_end,d.duration,s.price from subscriptions s
         left join states st on s.state_id=st.id left join bank_cards bc on s.card_id=bc.id left join durations d on s.duration_id=d.id"""
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