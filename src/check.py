def check_flower_by_name(results: tuple, flower_name: str):
    for items in results:
        for key in list(items.items())[1]:
            if items[key] == flower_name:
                return True
