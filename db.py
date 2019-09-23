import sqlite3


class DB:

    def __init__(self):
        self.con = sqlite3.connect("pay_planner_db.db")

    def get_subs_count(self):
        cur = self.con.cursor()
        cur.execute("select count(*) from subscriptions")
        result = cur.fetchone()[0]
        self.con.commit()
        cur.close()
        return result

    def get_all_subscriptions(self):
        cur = self.con.cursor()
        sql = """select s.service_name, st.name,bc.bank,bc.pay_system, bc.number,d.duration,
        s.price,s.term_end from subscriptions s
        left join states st on s.state_id=st.id left join bank_cards bc on s.card_id=bc.id 
        left join durations d on s.duration_id=d.id"""
        cur.execute(sql)
        result = cur.fetchall()
        self.con.commit()
        cur.close()
        return result

    def get_all_states(self):
        cur = self.con.cursor()
        sql = """select * from states"""
        cur.execute(sql)
        result = cur.fetchall()
        self.con.commit()
        cur.close()
        return result

    def get_all_durations(self):
        cur = self.con.cursor()
        sql = """select * from durations"""
        cur.execute(sql)
        result = cur.fetchall()
        self.con.commit()
        cur.close()
        return result

    def get_all_bank_cards(self):
        cur = self.con.cursor()
        sql = """select * from bank_cards"""
        cur.execute(sql)
        result = cur.fetchall()
        self.con.commit()
        cur.close()
        return result

    def add_subscription_to_db(self, t):
        cur = self.con.cursor()
        cur.execute("select count(*) from subscriptions")
        n = cur.fetchone()[0]
        self.con.commit()
        try:
            cur.execute("insert into subscriptions values(?,?,?,?,?,?,?)", [n, t[0], t[1], t[2], t[3], t[4], t[5]])
        except sqlite3.DatabaseErrori as err:
            print("Ошибка работы с БД "+ err)
        self.con.commit()
        cur.close()

    def __del__(self):
        self.con.close()