import models.model_category as model_category

def add_category(name, priority):
    try:
        model_category.add_category(name, priority)
    except Exception as e:
        return {'error': str(e)}
    return {'message': 'The category has been added successfully.'}

def update_category(category_id, category_name, priority):
    try:
        model_category.update_category(category_id, category_name, priority)
    except Exception as e:
        return {'error': str(e)}
    return {'message': 'The category information has been updated.'}

def remove_category(id):
    try:
        model_category.remove_category(id)
    except Exception as e:
        return {'error': str(e)}
    return {'message': 'The category has been removed successfully.'}

def list_categories():
    try:
        return_dict = model_category.get_category_list()
        if len(return_dict) == 0:
            return []
        return return_dict
    except Exception as e:
        return {'error': str(e)}
