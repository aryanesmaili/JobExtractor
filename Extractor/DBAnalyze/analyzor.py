import pandas as pd
import sqlalchemy as sa
from dotenv import load_dotenv
from os import getenv

load_dotenv()

conn_string = getenv('DB_PATH')
engine = sa.create_engine(conn_string)
df = pd.read_sql_table("processed_job_records", engine)

# Do something with the DataFrame:
print(df.head())
