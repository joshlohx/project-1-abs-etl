from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import URL

class PostgreSqlClient:

    def __init__(self, username:str, password:str, host:str, database_name:str, port: int = 5432):
        
        self.username = username,
        self.password = password,
        self.host = host,
        self.database_name = database_name
        self.driver = "postgresql+pg8000"
        self.port = port

        connection_url = URL.create(
            drivername = self.driver, 
            username = self.username,
            password = self.password,
            host = self.host, 
            port = self.port,
            database = self.database_name)
        
        self.engine = create_engine(connection_url)

    def create_table(self, metadata:MetaData):
        metadata.create_all(self.engine)

    def drop_table(self, table_name:str):
        self.engine.execute(f"drop table if exists {table_name}")

    def insert(self, dataframe, table):
        data = dataframe.to_dict(orient="records")
        insert_statement = postgresql.insert(table).values(data)

        self.engine.execute(insert_statement)

    def upsert(self, dataframe, table:Table):
        primary_key = [
            pk_column.name for pk_column in table.primary_key.columns.values()
        ]

        insert_statement = postgresql.insert(table).values(
            dataframe.to_dict(orient="records")
            )
        
        upsert_statement = insert_statement.on_conflict_do_update(
            index_elements = primary_key,
            set_={
            c.key: c
            for c in insert_statement.excluded
            if c.key not in primary_key
                }
            )

        self.engine.execute(upsert_statement)
