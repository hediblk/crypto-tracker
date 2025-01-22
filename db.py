import sqlite3

con = sqlite3.connect("cryptos.db")
cur = con.cursor()


def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS cryptos (ticker TEXT PRIMARY KEY, name TEXT, price REAL, last_update TEXT)")

def add_crypto(ticker, name):
    cur.execute("INSERT INTO cryptos (ticker, name, price, last_update) VALUES (?, ?, ?, ?)", (ticker, name, -1, "never"))
    con.commit()

def update_crypto(ticker, price):
    cur.execute("UPDATE cryptos SET price = ?, last_update = datetime('now') WHERE ticker = ?", (price, ticker))
    con.commit()

def get_crypto(ticker):
    cur.execute("SELECT * FROM cryptos WHERE ticker = ?", (ticker,))
    return cur.fetchone()

def get_all():
    cur.execute("SELECT * FROM cryptos")
    return cur.fetchall()




if __name__ == "__main__":
    create_table()
    con.close()
