import cx_Oracle

from .utils_config import oracle_lib_dir, oracle_client_info


class Oracle(object):

    def __init__(self):
        # Init
        cx_Oracle.init_oracle_client(lib_dir=oracle_lib_dir)
        self.connect()

    def connect(self):
        # Client
        self.client = cx_Oracle.connect(
            user=oracle_client_info["user"],
            password=oracle_client_info["password"],
            dsn=oracle_client_info["dsn"],
            encoding=oracle_client_info["encoding"]
        )
        # Cursor
        self.cursor = self.client.cursor()

    def execute(self, query):
        try:
            return self.cursor.execute(query)
        except:
            print("[INFO] reconnect oracle...")
            self.connect()
            return self.cursor.execute(query)


oracle = Oracle()
