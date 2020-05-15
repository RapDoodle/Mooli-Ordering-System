from models.DAO import DAO
from utils.exception import ValidationError

from utils.validation import is_rating, is_valid_length

def get_archive_index(value):
    # Clean input data
    value = str(value).strip()

    # Verift the input data
    # Archive only support string of length 1 to 255
    if not is_valid_length(value, 1, 255):
        raise ValidationError('Invalid length.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    search_sql = """SELECT archive_index FROM archive WHERE value = %(value)s"""
    cursor.execute(search_sql, {'value': value})
    result = cursor.fetchone()

    if result is not None:
        return result['archive_index']

    # When the archive library does not exist the given value, create on
    insert_sql = """INSERT INTO archive (value) VALUES (%(value)s)"""
    cursor.execute(insert_sql, {'value': value})
    cursor.execute(search_sql, {'value': value})
    result = cursor.fetchone()
    dao.commit()

    return result['archive_index']
