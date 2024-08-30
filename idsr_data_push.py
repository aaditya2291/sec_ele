from sqlalchemy import create_engine
import pandas as pd
from idsr.random_base64 import get_random_base64
from idsr.generate_df import get_decoded_df

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


idsr_data_push = get_decoded_df(get_random_base64(5000))

try:
    idsr_data_push.to_sql("idsr", con=db_engine(), if_exists="append", index=False)
except Exception as e:
    print(str(e))
