def validation_integer(usage):
    num = 0
    while True:
        try:
            num = int(input(usage))
        except ValueError:
            print("Please enter a valid integer")
            continue
        if num > 0:
            print(f'You entered: {num}')
            break
        else:
            print('Please enter a positive integer (min:1)')    
    return num

