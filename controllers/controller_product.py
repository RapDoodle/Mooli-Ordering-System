import models.model_product as m

def add_product(*args, **kwargs):
    try:
        m.add_product(*args, **kwargs)
    except Exception as e:
        return {'error': str(e)}
    return {'message': 'The product has been added successfully.'}

def edit_product(*args, **kwargs):
    try:
        m.update_product(*args, **kwargs)
    except Exception as e:
        return {'error': str(e)}
    return {'message': 'The product information has been updated.'}

def remove_product(product_id):
    try:
        m.remove_product(product_id)
    except Exception as e:
        return {'error': str(e)}
    return {'message': 'The product has been removed successfully.'}

def get_products_by_id(product_id):
    try:
        return_dict = m.find_product('product_id', product_id)
        if len(return_dict) == 0:
            return []
        return return_dict
    except Exception as e:
        return {'error': str(e)}

def get_products_by_category(category_name):
    try:
        return_dict = m.get_products('category_name', category_name)
        if len(return_dict) == 0:
            return []
        return return_dict
    except Exception as e:
        return {'error': str(e)}

def get_all_products():
    try:
        return m.get_products('all')
    except Exception as e:
        return {'error': str(e)}

def get_product_by_name(product_name):
    try:
        return_dict = m.find_product('product_name', product_name)
        return return_dict
    except Exception as e:
        return {'error': str(e)}

def get_product_by_product_id(product_id):
    try:
        return m.find_product('product_id', product_id)
    except Exception as e:
        return {'error': str(e)}
