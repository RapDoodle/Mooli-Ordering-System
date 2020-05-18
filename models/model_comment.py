from models.DAO import DAO
from utils.exception import ValidationError
from utils.validation import is_rating, is_valid_length
from models.shared import find_user, find_product
import utils.cache as cache

def add_comment(user_id, product_id, rating, body = ''):
    # Clean input data
    user_id = str(user_id).strip()
    product_id = str(product_id).strip()
    rating = str(rating).strip()
    body = str(body).strip()

    # Verify the rating
    if not is_rating(rating):
        raise ValidationError('Invalid rating.')

    # Verify the length of body
    # The maximum length of the body is 140 characters (like a tweet)
    # TO-DO: Front-end must set the limit for the number of characters
    if not is_valid_length(body, 0, 140):
        raise ValidationError('Invalid body length.')

    # Verify the validity of the user_id
    user = find_user(method = 'id', param = user_id)
    if user is None:
        raise ValidationError('user not found.')

    # Verify the product_id
    product = find_product('product_id', product_id)
    if product is None:
        raise ValidationError('Product not found.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """INSERT INTO comment (
        user_id,
        product_id,
        rating,
        body
    ) VALUES (
        %(user_id)s,
        %(product_id)s,
        %(rating)s,
        %(body)s
    )"""
    cursor.execute(sql, {'user_id': user_id,
                        'product_id': product_id,
                        'rating': rating,
                        'body': body})
    dao.commit()

    # Update the ratings to the caching system
    update_ratings_cache(product_id)

def remove_comment(comment_id):
    # Clean the input data
    comment_id = str(comment_id).strip()

    # Check does the comment exists
    if find_comment(comment_id) is None:
        raise ValidationError('Comment not found.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Delete comment from the database
    sql = """DELETE FROM comment WHERE comment_id = %(comment_id)s"""
    cursor.execute(sql, {'comment_id': comment_id})
    dao.commit()

    # Update the ratings to the caching system
    update_ratings_cache(product_id)

def find_comment(comment_id):
    # Clean the input data
    comment_id = str(comment_id).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query the comment
    sql = """SELECT * FROM comment WHERE comment_id = %(comment_id)s"""
    cursor.execute(sql, {'comment_id': comment_id})
    result = cursor.fetchone()
    return result

def get_comments(param = '', method = 'product_id', limit = 0, offset = 0):
    if method not in ['product_id', 'all']:
        raise ValidationError('Invalid method.')

    # Clean the input data
    param = str(param).strip()
    limit = str(limit).strip()
    offset = str(offset).strip()

    if not limit.isdecimal() or not offset.isdecimal():
        raise ValidationError('Invalid input.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = ''
    if method == 'all':
        sql = """SELECT * FROM comment ORDER BY comment_id ASC"""
    else:
        # Find comments by product id
        sql = """SELECT * FROM comment WHERE product_id = %(param)s ORDER BY comment_id DESC"""
    if not int(limit) == 0:
        sql += ' LIMIT ' + limit + ' OFFSET ' + offset
    cursor.execute(sql, {'param': param})
    result = cursor.fetchall()
    return result

def get_product_ratings(product_id):
    """The function is used to get the ratings of a product

    Parameters:
    product_id -- the id of the product
    """
    # Clean the input data
    product_id = str(product_id).strip()

    # Verify the product_id
    product = find_product('product_id', product_id)
    if product is None:
        raise ValidationError('Product not found.')

    avg_ratings = cache.get('rating_' + product_id)
    if avg_ratings is None:
        avg_ratings = update_ratings_cache(product_id)

    return avg_ratings

def update_ratings_cache(product_id):
    """The function will calculate the average stars rating of the given product
    and save it to the caching  system.

    Parameters:
    product_id -- the id of the product
    """
    # Clean the input data
    product_id = str(product_id).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query the comment
    sql = """SELECT FORMAT(AVG(rating), 2) AS avg FROM comment WHERE product_id = %(product_id)s"""
    cursor.execute(sql, {'product_id': product_id})
    avg_ratings = cursor.fetchone()['avg']

    cache.set('rating_' + product_id, avg_ratings)

    return avg_ratings