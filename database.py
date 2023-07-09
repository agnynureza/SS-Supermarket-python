from sqlalchemy import create_engine 
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

# Create Engine
# Configuration Connection to SQLite
engine = create_engine('sqlite:///super-cashier.sqlite', echo=True)

# Manage Tables 
base = declarative_base()

class Customer(base):
    
    __tablename__ = "sc_customer"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __init__(self, name):
        self.name = name
        
class Transaction(base):
    
    __tablename__ = "sc_transaction"
    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    item_amount = Column(Integer)
    price = Column(Integer)
    total_price = Column(Integer)
    discount = Column(Integer)
    price_after_discount = Column(Integer)
    created_at = Column(Date)
    customers = relationship(Customer, secondary = 'sc_item_transaction')
    
    def __init__(self, item_name, item_amount, price, total_price, discount, price_after_discount, created_at):
        self.item_name = item_name
        self.item_amount = item_amount
        self.price = price
        self.total_price = total_price
        self.discount = discount
        self.price_after_discount = price_after_discount
        self.created_at = created_at

class Item_Transaction(base):
    __tablename__ = 'sc_item_transaction'
    customer_id = Column(Integer, ForeignKey('sc_customer.id'), primary_key = True)
    transaction_id = Column(Integer, ForeignKey('sc_transaction.id'), primary_key = True)
    
    
    
base.metadata.create_all(engine)