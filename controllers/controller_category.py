import models.model_category as model_category

def add_category(name, priorty):
    try:
        model_category.add_category(name, priorty)
    except Exception as e:
        return {'error': str(e)}
    return {'message': 'The category has been added successfully.'}

def remove_category(name):
    try:
        model_category.remove_category(name)
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
