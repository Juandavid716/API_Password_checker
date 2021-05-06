
def create_table(name_table, con):
    cur = con.cursor() 
    query = """
     CREATE TABLE IF NOT EXISTS {} (
        dimension TEXT PRIMARY KEY NOT NULL,
        probability VARCHAR(30) NOT NULL)""".format(name_table)

    cur.execute(query)
    cur.execute("DELETE FROM {}".format(name_table))
    con.commit()

def create_size(con, length_x):
    cur = con.cursor() 
    query="""
    CREATE TABLE IF NOT EXISTS length_table (
        length_t INTEGER PRIMARY KEY NOT NULL DEFAULT '{}'
        )""".format(length_x)
    cur.execute(query)
    cur.execute("INSERT INTO length_table (length_t) VALUES ({}) ON CONFLICT  (length_t) DO NOTHING".format(length_x))
    con.commit()

def create_table_hash(con):
    cur = con.cursor() 
    query = """
     CREATE TABLE IF NOT EXISTS {} (
        id SERIAL,
        hash_t VARCHAR(100) NOT NULL)""".format("hash_table")

    cur.execute(query)
    con.commit()
    #cur.execute("DELETE FROM {}".format(name_table))