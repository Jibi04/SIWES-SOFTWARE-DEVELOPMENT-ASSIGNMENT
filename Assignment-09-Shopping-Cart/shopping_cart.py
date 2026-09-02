def shopping_cart_system():
    products = []
    line = 40 * '*'
    options = f"""
    Hi, what would you like to do today?
(1) - Add item
(2) - Remove item
(3) - View Cart
(4) - Total products
(5) - exit
"""
    print(line)
    print('\t\tMENU\t\t')
    print(line)

    while True:
        request = get_user_values(f'{options}:> ')
        if request == 5:
            break
        elif request == 4:
            print('Item count: ', len(products))
            if should_continue():
                continue
            else: break

        elif request == 1:
            product_name = input('Product Name: ').strip()
            products.append(product_name)
            print(f'{product_name} added to cart.')
            if should_continue():
                continue
            else: break

        elif request == 2:
            product_name = input('Product Name: ').strip()
            if product_name not in products:
                print(f'{product_name} not in cart.')
                break
            else:
                products.remove(product_name)
                print(f'{product_name} removed from cart.')
                if should_continue():
                    continue
                else: break
        elif request == 3:
            if len(products) <= 0:
                print('Your cart is empty.')
                continue
            for i, item in enumerate(products):
                print(f'{i}: {item}')
            break
        else:
            print('Invalid response, (5) to exit')
            continue
        
def should_continue():
    response = int(input('Would you like to do anything else? (1 - YES, 0 - NO): '))
    return bool(response)

def get_user_values(msg: str):
    while True:
        try:
            res = input(f'{msg}')
            val = float(res)
            return val
        except ValueError:
            print(f'Invalid Value expected an Integer/Decimal but got \'{type(res).__name__}\'')
            continue

if __name__ == '__main__':
    shopping_cart_system()
