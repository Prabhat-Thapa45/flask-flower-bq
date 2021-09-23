def check_flower_by_name(results: tuple, flower_name: str) -> bool:
    """Checks if the given flower_name is available in results if yes returns True else False
    Args:
        results (tuple): a tuple consisting of dict type as elements from rows of sql tables.
            e.g: for table with one row ({'id': 1, 'flower_name': 'Rose', 'price': 6.5, 'quantity': 21},)
        flower_name (str): name of a flower
    returns:
        boolean 
    """
    for items in results:
        for key in list(items.items())[1]:
            if items[key] == flower_name:
                return True
            else:
                return False


def int_convertor(value: str) -> int:
    """Converts str type to int type
    Args:
        value (str): strings to be converted to int type
    return:
        int
    raises:
        ValueError: if value is str that cannot be converted into int
    """
    try:
        return int(value)
    except ValueError:
        return 0


