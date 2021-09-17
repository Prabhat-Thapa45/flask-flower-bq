def choose_menu():
    print("Choose Options...\n1. View Menu\n2. Add Flower\n3. Delete Flower\n4. Purchase Flower\n5. View Order History\n6. Exit")


def display_menu(menu1):
    print("Code  |  Quantity  |  Flowers")
    separate_line()
    for i in menu1.keys():
        print(" ", i, " -->", "  ", menu1[i][0], "   -->", " ",menu1[i][1])


def display_order_history(history):
    print(history)


def show_option():
    print("1. Confirm\n2. Alternative\n0. CANCEL\n")


def thanks_for_visiting():
    print("------Thanks for visiting-------")


def invalid_input():
    print("Invalid Input...")


def add_successfully():
    print("Flower Added Successfully...🌻")


def del_successfully():
    print("Flower Deleted Successfully...🌻")


def congratulation():
    print("Congratulation...Order Placed...🥰")


def visit_again():
    print("Ugh..! Please visit again...😥")


def separate_line():
    print("--------------------------------")
