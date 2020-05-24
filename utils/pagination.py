import math

def  get_page_numbers(length, current = 1, limit = 20, show = 8):
    try:
        length = int(length)
        current = int(current)
        limit = int(limit)
        show = int(show)
    except:
        return [1]
    if length < limit:
        return [1]
    pages = math.ceil(length / limit)

    # Control the overflow of page numbers
    pagination = []
    lower = current - (show / 2)
    upper = current + (show / 2)
    if lower <= 0:
        upper = min(upper + abs(lower), pages)
        lower = 1
    if upper > pages:
        lower = max(lower - (upper - pages), 1)
        upper = pages

    # Make sure they are int
    lower = int(lower)
    upper = int(upper)

    # List out the page numbers that need to be displayed
    # Problems: - jinja2 does not support the full python env within
    #             its own environment
    #           - use str instead of int for safer comparison
    if lower != 1:
        pagination.append('1')
        pagination.append('None')
    for i in range(lower, upper + 1):
        pagination.append(str(i))
    if upper != pages:
        pagination.append('None')
        pagination.append(str(pages))
    return pagination
    