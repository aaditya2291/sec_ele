from sqlalchemy import create_engine
import pandas as pd


def db_engine():
    try:
        host = "89.116.20.197"
        port = "3306"
        db_name = "criskledatapoints"
        username = "criskledpsql"
        password = "5PeHydQqj4xqixUV76l4"
        con_str = "mysql+pymysql://{}:{}@{}:{}/{}".format(username, password, host, port, db_name)
        engine = create_engine(con_str, paramstyle="format")
        return engine
    except Exception as ex:
        print(str(ex))

query = """select * from idsr"""

idsr_data_fetch = pd.read_sql(query, con=db_engine())