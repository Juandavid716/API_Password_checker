
def create_table(name_table, cur):
    query = """
     CREATE TABLE IF NOT EXISTS {} (
        dimension TEXT PRIMARY KEY NOT NULL,
        probability VARCHAR(30) NOT NULL)""".format(name_table)

    cur.execute(query)
    cur.execute("DELETE FROM {}".format(name_table))

def create_size(con, length_x):
    cur = con.cursor() 
    query="""
    CREATE TABLE IF NOT EXISTS length_table (
        length_t INTEGER PRIMARY KEY NOT NULL DEFAULT '{}'
        )""".format(length_x)
    cur.execute(query)
    cur.execute("INSERT OR IGNORE INTO length_table (length_t) VALUES (?)",(length_x,))
    con.commit()

def create_table_hash( cur):
    query = """
     CREATE TABLE IF NOT EXISTS {} (
        hash_t VARCHAR(30) NOT NULL)""".format("hash_table")

    cur.execute(query)
    #cur.execute("DELETE FROM {}".format(name_table))