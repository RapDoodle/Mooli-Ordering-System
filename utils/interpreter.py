order_status_dictionary = {
    'CANC': 'cancelled',
    'PEND': 'pending',
    'PROC': 'processing',
    'REDY': 'ready for pickup',
    'DONE': 'done',
    'REDD': 'redeemed',
    'REFN': 'refunded'
}

def interprete_order_status(status, capitalize = False):
    status = str(status).upper()
    try:
        result = order_status_dictionary[status]
    except:
        result = 'unknown'
    if capitalize:
        result = result.capitalize()
    return result
    
