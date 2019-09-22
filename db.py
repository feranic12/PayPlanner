import sqlite3


class DB:

    def __init__(self):
        self.con = sqlite3.connect("pay_planner_db.db")

    def get_all_subscriptions(self):
        cur = self.con.cursor()
        sql = """select s.service_name, st.name,bc.bank,bc.number,s.term_end,d.duration,s.price from subscriptions s
         left join states st on s.state_id=st.id left join bank_cards bc on s.card_id=bc.id left join durations d on s.duration_id=d.id"""
        try:
            cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print("Ошибка работы с базой данных"+ err)
        else:
            print ("Успех")
            result = cur.fetchall()
            self.con.commit()
            cur.close()
            return result

    def get_all_durations(self):
        cur = self.con.cursor()
        sql = """select * from durations"""
        try:
            cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print("Ошибка работы с базой данных" + err)
        else:
            print ("Успех")
            result = cur.fetchall()
            self.con.commit()
            cur.close()
            return result

    def get_all_bank_cards(self):
        cur = self.con.cursor()
        sql = """select * from bank_cards"""
        try:
            cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print("Ошибка работы с базой данных" + err)
        else:
            print("Успех")

        result = cur.fetchall()
        self.con.commit()
        cur.close()
        return result

    def add_subscription_to_db(self, t):
        cur = self.con.cursor()
        try:
            cur.execute("insert into subscriptions values(?,?,?,?,?,?)", [t[0], t[1], t[2], t[3], t[4], t[5]])
        except sqlite3.DatabaseError as err:
            print("Ошибка работы с базой данных" + err)
        self.con.commit()
        cur.close()

    def __del__(self):
        self.con.close()