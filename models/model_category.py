from models.DAO import DAO

def add_category(category_name, priorty):
    dao = DAO()
    cursor = dao.cursor()
    if category_name and priorty:
        sql = """INSERT INTO category (
            category_name,
            priority
        ) VALUES (
            %(category_name)s,
            %(priorty)s
        )"""
        cursor.execute(sql, {'category_name': category_name, 'priorty': priorty})
        dao.commit()
