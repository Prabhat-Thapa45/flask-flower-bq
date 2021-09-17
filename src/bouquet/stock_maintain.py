from src.bouquet.utility.printing import add_successfully, del_successfully, invalid_input


class FlowerInventory:

    def add_flower(self, menu1):  # function for adding flower to dict...
        flower_code = input("Enter flower Code: ").upper()
        quantity = input("Enter Quantity : ")
        flower_name = input("Enter flower Name: ").capitalize()

        if quantity.isdigit():  # checking whether the quantity is number or not...if yes, then adding to dict...
            menu1[flower_code] = (quantity, flower_name)
            add_successfully()
        else:
            invalid_input()
            o1 = FlowerInventory
            o1.add_flower(self, menu1)

    def del_flower(self, menu1):  # function for deleting flower to dictionary...
        flower_code = input("Enter flower Code : ").upper()
        if flower_code in menu1.keys():  # checking the flower is in dict or not...if yes, then deleting from dict...
            del menu1[flower_code]
            del_successfully()
        else:
            invalid_input()
            o1 = FlowerInventory
            o1.del_flower(self, menu1)

    def deducting_from_stock(self, menu1, stock_bouquet):  # for deducting the quantity which is ordered
        key1 = []
        value1 = []
        for i in stock_bouquet:
            if i not in key1:
                key1.append(i)
                value1.append(stock_bouquet.count(i))

        d = dict(zip(key1, value1))
        for i in key1:
            menu1[i][0] = menu1[i][0] - d[i]
