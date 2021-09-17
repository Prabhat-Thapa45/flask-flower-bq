from collections import Counter
from flask import flash


# def take_order(order, result):
#     order = list(order.lower())
#     order_dict = dict(Counter(order))
#     result_dict = {}
#     flower_not_available = ""
#     limited_flower_dict = {}
#     # result is a tuple having dict as items eg ({"a": 3}, {"b": 4})
#     # we are converting above tuple into single dict as result_dict = {"a": 3, "b": 4}
#     for item in result:
#         for flower, quantity in item.items():
#             result_dict[flower] = quantity
#     # checking if we have flowers in stock
#     for flower, quantity in order_dict.items():
#         try:
#             result_dict[flower]
#         except KeyError:
#             flower_not_available += flower
#         else:
#             if result_dict[flower] > order_dict[flower]:
#                 result_dict[flower] -= quantity
#             else:
#                 limited_flower_dict[flower] = result_dict[flower]
#     return [flower_not_available, result_dict, limited_flower_dict]
#
#





# def check_order(order_dict):
#     for flower, quantity in order_dict.items:
#         if




