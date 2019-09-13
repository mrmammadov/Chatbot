import psycopg2


class DBConnect():

    def __init__(self, dbname,user, password,host):
        self.dbname = dbname
        self.dbname = dbname
        self.dbname = dbname
        self.dbname = dbname

    def db_connection(self):
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)

    def end_connection(self):
        self.conn.close()

    def update_bad_conv(self):
        self.db_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT bad_conv FROM messages LIMIT 1;")
        counter = self.cur.fetchone()[0]
        counter = counter + 1
        self.cur.execute("UPDATE messages SET bad_conv = %s", [counter])
        self.conn.commit()
        self.cur.close()
        self.end_connection()

    def update_good_conv(self):
        self.db_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT good_conv FROM messages LIMIT 1;")
        counter = self.cur.fetchone()[0]
        counter = counter + 1
        self.cur.execute("UPDATE messages SET good_conv = %s", [counter])
        self.conn.commit()
        self.cur.close()
        self.end_connection()
