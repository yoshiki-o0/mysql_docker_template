from app import model


def main():
    """Connect, Check"""
    mysqlmodel = model.MysqlModel()
    mysqlmodel.connect_database()
    mysqlmodel.check_database_existance()

    """Create, Insert"""
    mysqlmodel.create_table()
    mysqlmodel.insert_data()
    mysqlmodel.insert_data()

    """Conclude"""
    mysqlmodel.close_database()


if __name__ == "__main__":
    main()