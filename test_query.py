from app import model

def main():
    """Connect, Check"""
    mysqlmodel = MysqlModel()
    mysqlmodel.connect_database()
    mysqlmodel.check_database_existance()

    """Query"""
    mysqlmodel.query_data()

    """Conclude"""
    mysqlmodel.close_database()

if __name__ == "__main__":
    main()