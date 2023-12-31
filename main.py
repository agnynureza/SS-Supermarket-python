""" This Module is the main process self-service system for shopping.
    
you can run this module after initialize database and table SQLite,
execute database.py, after .sqlite file created you can 
run main.py.

"""

# Import tabulate library, function tabulate to display data in table format
from tabulate import tabulate
#import sys to access force exit system
import sys
#import model for manipulation data
import model as m
#import validation for validate payload input
import validation as v


def loading_line():
    print("..................................")

def create_new_customer():
    """ This Function will create new costumer to database.

    """
    try:
        name = input("Enter name:")
        
        # create new costumer
        m.create_new_customer(name)
        
        loading_line()
        print(f'Success Create Customer {m.CUSTOMER_DATA.name}, Happy Shopping')
    except Exception as e:
        loading_line()
        print(f"Error when create costumer {e}")

    #Back to main menu
    main_menu()

def load_registered_customer():
    """ This Function will load exist costumer who already registered before.

    """
    try:
        id = input("Enter Customer ID:")
        
        # search user who already register to set the session
        isFound = m.search_customer_by_id(id)
        loading_line()
        if isFound:
            print(f"Welcome {m.CUSTOMER_DATA.name}, Happy Shopping again")
        else:
            print("Customer Not Found, Please Sign up new Customer")

    except Exception as e:
        loading_line()
        print(f"Error when get costumer data {e}")
    
    #Back to main menu
    main_menu()

def check_session_customer_active():
    """ This Function will check session login costumer.

    """
    print(f"Customer ID: {m.CUSTOMER_DATA.id} | Customer Name: {m.CUSTOMER_DATA.name}")

def add_new_item():
    """ This Function will add new item after login costumer id

    """
    try:
        item_name = input ("Enter item name:")
        item_amount = v.validation_integer("Enter item amount:")
        item_price = v.validation_integer("Enter item price:")
        
        result = m.add_new_item(item_name, item_amount, item_price)
        loading_line()
        if result:
            print(f"Success Add item {item_name} to Cart")
        else:
            print(f"Error Duplicate Item {item_name} on Cart, Use another Task for the changes")
    except Exception as e:
        loading_line()
        print(f"Error when add item {e}")
        
    #Back to main menu
    main_menu()

def update_item_name():
    """ This Function will update with new item name data by item name

    """
    try:
        item_name = input("Enter Current item name:")
        new_item_name = input("Enter New item Name:")
        
        result = m.update_item_name(item_name, new_item_name)
        loading_line()
        if result:
            print(f"Success Update item name for {new_item_name}")
        else:
            print(f"Error Item Name Not Found")
    except Exception as e:
        loading_line()
        print(f"Error when update item name {e}")
        
    #Back to main menu
    main_menu()
    
def update_item_price():
    """ This Function will update with new item price data by item name

    """
    try:
        item_name = input("Enter Current item name:")
        new_item_price = v.validation_integer("Enter item price:")
        
        result = m.update_item_price(item_name, new_item_price)
        loading_line()
        if result:
            print(f"Success Update item price for {item_name}")
        else:
            print(f"Error Item Name Not Found")
    except Exception as e:
        loading_line()
        print(f"Error when update item price {e}")
        
    #Back to main menu
    main_menu()

def update_item_quantity():
    """ This Function will update with new item quantity data by item name

    """
    try:
        item_name = input("Enter Current item name:")
        new_item_quantity = v.validation_integer("Enter item amount:")
        
        result = m.update_item_quantity(item_name, new_item_quantity)
        loading_line()
        if result:
            print(f"Success Update item amount for {item_name}")
        else:
            print(f"Error Item Name Not Found")
    except Exception as e:
        loading_line()
        print(f"Error when update item amount {e}")
        
    #Back to main menu
    main_menu()
    
def delete_item():
    """ This Function will delete item by item name

    """
    try:

        item_name = input("Enter item name:")
        
        # delete one item from cart
        result = m.delete_item_for_cart(item_name)
        loading_line()
        if result:
            print(f"Success delete item {item_name} from Cart")
        else:
            print(f"Error Item Name Not Found")
    except Exception as e:
        loading_line()
        print(f"Error when delete item {e}")
        
    #Back to main menu
    main_menu()

def reset_all_item():
    """ This Function will reset transaction, it makes cart empty

    """
    
    # empty the cart
    m.reset_transaction()
    print(f"Success Reset Transaction, Carts are Empty")
    
    #Back to main menu
    main_menu()

def check_order():
    """ This Function will display all item on cart

    """
    # construct object on cart to become nested list to display order
    headers = ['No', 'Item Name', 'Item Amount', 'Item Price', 'Total Price']
    data = m.convert_list_of_dict_to_list_value()
    print(tabulate(data,headers))
    loading_line()

    # Back to main menu
    main_menu()

def check_out():
    """ This Function will Insert item on cart to database

    """
    try:
        # insert list of item on cart to database
        m.insert_to_table_transaction()
        loading_line()
        print(f"Success Check Out {len(m.TEMPORARY_ITEM_TRANSANCTION)} Item, Thank you for Shopping")
        m.TEMPORARY_ITEM_TRANSANCTION = []
    except Exception as e:
        loading_line()
        print(f"Error when delete item {e}")
    
    #Back to main menu
    main_menu()

def check_history_shopping():
    """ This Function will display list item complete with discount price and purcashed date

    """
    data_transaction = m.get_all_item_by_customer_id()
    list_items = []
    
    # iterate object data_transaction
    # construct object become nested list for display history
    for i, item in enumerate(data_transaction):
        list_items.append([i+1, 
                            item.item_name, 
                            item.item_amount, 
                            item.price,
                            item.total_price, 
                            item.discount, 
                            item.price_after_discount,
                            item.created_at
                           ])

    headers = ['No', 'Item Name', 'Item Amount', 'Item Price', 'Total Price', 'Discount', 'Total after Discount', 'Purchased Date']
    print("~ List History Shopping ~")
    check_session_customer_active()
    print(tabulate(list_items,headers))
    loading_line()

    # Back to main menu
    main_menu()
  
def exit():
    """ This Function access system to give signal exit
    """
    print("""
    ~ Thank you for using Super Cashier. Tiada Kesan Tanpa Kehadiran mu ~
    """)
    sys.exit(0)

# MAIN MENU - Super Cashier
def main_menu():
    # User interface layout
    print()
    print("""........... Welcome to Super Cashier System........... 
    1. Create New Customer
    2. Load registered Customer
    3. Check Session Customer
    4. Add New Item
    5. Update Item Name
    6. Update Item Quantity
    7. Update Item Price
    8. Delete Item
    9. Reset Transaction
    10. Check Order Item
    11. Check Out Item
    12. Check History Shopping
    13. Exit
    """)
    
    # Prompting user to enter any task above 
    choice = int(input("Enter task no: "))
    loading_line()
  
    # exit program
    if choice==13:
        exit()
        
    # After user enter task no, respective task functions will be executed
    user_task_list = [1, 2]
    if m.CUSTOMER_DATA is None and choice not in user_task_list:
        print("please sign up customer data before continue another task")
        main_menu()
        
    if choice==1:
        create_new_customer()
    elif choice==2:
        load_registered_customer()
    elif choice==3:
        check_session_customer_active()
    elif choice==4:
        add_new_item()
    elif choice==5:
        update_item_name()
    elif choice==6:
        update_item_quantity()
    elif choice==7:
        update_item_price()
    elif choice==8:
        delete_item()
    elif choice==9:
        reset_all_item()
    elif choice==10:
        check_order()
    elif choice==11:
        check_out()
    elif choice==12:
        check_history_shopping()
    else:
        print("invalid task number, please re-enter task")
   
    # If user key in no outside of available inputs, main menu will be displayed
    main_menu()

# Displaying main menu when main.py file is executed on terminal
main_menu()