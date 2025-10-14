from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import URL

class PostgreSqlClient:

    def __init__(self, username:str, password:str, host:str, database_name:str, port: int = 5432):
        
        self.username = username
        self.password = password
        self.host = host
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

    def create_table(self, metadata:MetaData) -> None:
        metadata.create_all(self.engine)

    def drop_table(self, table_name:str) -> None:
        self.engine.execute(f"drop table if exists {table_name}")

    def overwrite(self, data:list[dict], table:Table, metadata: MetaData) -> None:
        self.drop_table(table_name=table.name)
        self.insert(data=data, table=table, metadata=metadata)

    def insert(self, data:list[dict], table:Table, metadata: MetaData) -> None:
        metadata.create_all(self.engine)
        insert_statement = postgresql.insert(table).values(data)
        self.engine.execute(insert_statement)

    def upsert(self, data:list[dict], table:Table, metadata: MetaData) -> None:
        metadata.create_all(self.engine)
        primary_key = [
            pk_column.name for pk_column in table.primary_key.columns.values()
        ]

        insert_statement = postgresql.insert(table).values(data)
        
        upsert_statement = insert_statement.on_conflict_do_update(
            index_elements = primary_key,
            set_={
            c.key: c
            for c in insert_statement.excluded
            if c.key not in primary_key
                }
            )

        self.engine.execute(upsert_statement)
