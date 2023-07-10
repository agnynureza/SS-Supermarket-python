""" This Module is data manipulation.
    
all the process to database or temporary data in application will
process in this module

"""

import database as db
from sqlalchemy.orm import sessionmaker
from datetime import date

# New Session 
Session = sessionmaker(bind=db.engine)
session = Session()

# Global Variabel
CUSTOMER_DATA = None
TEMPORARY_ITEM_TRANSANCTION = []

def create_new_customer(name):
    """ create_new_customer
    
    connect to database to store costumer data and 
    set the costumer ID as identifier for shopping
    """
    
    customer = db.Customer(name = name)
    session.add(customer)    
    session.commit()
    session.refresh(customer)
    
    global CUSTOMER_DATA 
    CUSTOMER_DATA = customer
    
    global TEMPORARY_ITEM_TRANSANCTION
    TEMPORARY_ITEM_TRANSANCTION = []
def search_customer_by_id(id):
    """ search_customer_by_id
    
    connect to database to search exist costumer and
    flush temporary cart on application because change session data
    """
    
    result = session.query(db.Customer).filter(db.Customer.id == id).all()
    if result:
        global CUSTOMER_DATA
        CUSTOMER_DATA = result[0]
        
        global TEMPORARY_ITEM_TRANSANCTION
        TEMPORARY_ITEM_TRANSANCTION = []
    
        return True
    else:
        return False

def search_item_on_cart(name):
    """ search_item_on_cart
    
    helpful for filtering duplicate item on cart or find exist item before processing
    """
    global TEMPORARY_ITEM_TRANSANCTION
    
    key = "item_name"
    val = name
    for i, list_item in enumerate(TEMPORARY_ITEM_TRANSANCTION):
        if list_item[key] == val:
            return i    
        
    return None


def add_new_item(name, amount, price):
    """ add_new_item
    
    add item to temporary transaction (CART)
    """
    global TEMPORARY_ITEM_TRANSANCTION
    
    # Check item_name before adding new one
    index = search_item_on_cart(name)
    if index is not None:
        return False
    
    TEMPORARY_ITEM_TRANSANCTION.append({
        "item_name": name, 
        "item_amount": amount,
        "item_price": price,
        "total_price": amount*price,
    })
    
    return True

def update_item_name(name, new_name):
    """ update_item_name
    
     will update item object with identifier item name
    """
    global TEMPORARY_ITEM_TRANSANCTION
    
    # Check item_name before adding new one
    index = search_item_on_cart(name)
    if index is None:
        return False
    
    TEMPORARY_ITEM_TRANSANCTION[index]["item_name"] = new_name
    
    return True


def update_item_price(name, new_price):
    """ update_item_price
    
     will update item object with identifier item name
    """

    global TEMPORARY_ITEM_TRANSANCTION
    
    # Check item_name
    index = search_item_on_cart(name)
    if index is None:
        return False
    
    TEMPORARY_ITEM_TRANSANCTION[index]["item_price"] = new_price
    TEMPORARY_ITEM_TRANSANCTION[index]["total_price"] = new_price*TEMPORARY_ITEM_TRANSANCTION[index]["item_amount"] 
    
    return True


def update_item_quantity(name, new_quantity):
    """ update_item_quantity
    
     will update item object with identifier item name
    """
    
    global TEMPORARY_ITEM_TRANSANCTION
    
    # Check item_name before adding new one
    index = search_item_on_cart(name)
    if index is None:
        return False
    
    TEMPORARY_ITEM_TRANSANCTION[index]["item_amount"] = new_quantity
    TEMPORARY_ITEM_TRANSANCTION[index]["total_price"] = new_quantity*TEMPORARY_ITEM_TRANSANCTION[index]["item_price"] 
    
    return True

def delete_item_for_cart(name):
    """ delete_item_for_cart
    
     remove object item for temporary transaction
    """
    
    global TEMPORARY_ITEM_TRANSANCTION
    
    # Check item_name before adding new one
    index = search_item_on_cart(name)
    if index is None:
        return False
    
    del TEMPORARY_ITEM_TRANSANCTION[index]
    
    return True

def reset_transaction():
    """ reset_transaction
    
     remove all the object on temporary transaction
    """
    global TEMPORARY_ITEM_TRANSANCTION
    TEMPORARY_ITEM_TRANSANCTION = []
    
def convert_list_of_dict_to_list_value():
    """ convert_list_of_dict_to_list_value
    
    change data structure from object to list of value
    """
    global TEMPORARY_ITEM_TRANSANCTION
    list_values = []
    
    for i, list_item in enumerate(TEMPORARY_ITEM_TRANSANCTION): 
        list_values.append([i+1] + list(list_item.values()))
    
    return list_values

def add_discount_item(total_price):
    """ add_discount_item
    
    calculate discount each item
    """
    if total_price > 500_000:
        return total_price * (7/100)
    elif total_price > 300_000:
        return total_price * (6/100)
    elif total_price > 200_000:
        return total_price * (5/100)
    else:
        return 0

def insert_to_table_transaction():
    """ add_discount_item
    
    insert to table transaction and append to relation table item_transaction
    """
    for _, list_item in enumerate(TEMPORARY_ITEM_TRANSANCTION):
        discount = add_discount_item(list_item["total_price"])
        price_after_discount = list_item["total_price"] - discount
        
        transaction = db.Transaction(
            list_item["item_name"], 
            list_item["item_amount"], 
            list_item["item_price"],
            list_item["total_price"], 
            discount, 
            price_after_discount,
            date.today()
            )
        transaction.customers.append(CUSTOMER_DATA)
        session.add(transaction)
    session.commit()

def get_all_item_by_customer_id():
    """ get_all_item_by_customer_id
    
    get all record of history shopping
    """
    return session.query(db.Transaction).\
        join(db.Item_Transaction, db.Item_Transaction.transaction_id == db.Transaction.id).\
        join(db.Customer, db.Customer.id == db.Item_Transaction.customer_id).\
        filter(db.Customer.id == CUSTOMER_DATA.id)
        