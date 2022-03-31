import sqlite3

def db_factory(dbname):
    return sqlite3.connect('D:/myProjects/myKiwoom/'+dbname)

def df_to_db(df, dbname, table):
    try:
        db = db_factory(dbname)
        print('connected to db')
    except Error as e:
        print(e)
    
    try:
        df.to_sql(table, db, if_exists = 'replace')
        print('saved requested data in db')
    except Error as e:
        print(e)


