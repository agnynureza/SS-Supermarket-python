""" This Module for validation input payload.
    
middleware to validate integer data type

"""
def validation_integer(usage):
    num = 0
    while True:
        try:
            num = int(input(usage))
        except ValueError:
            print("Please enter a valid integer")
            continue
        if num > 0:
            break
        else:
            print('Please enter a positive integer (min:1)')    
    return num

