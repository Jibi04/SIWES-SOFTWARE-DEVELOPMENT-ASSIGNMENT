from helper_functions import get_integer_input_from_user, should_continue

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
        request = get_integer_input_from_user(f'{options}:> ')
        if request == 5:
            break
        elif request == 4:
            print('Item count: ', len(products))
            if not should_continue():
                break

        elif request == 1:
            product_name = input('Product Name: ').strip()
            products.append(product_name)
            print(f'{product_name} added to cart.')
            if not should_continue():
                break

        elif request == 2:
            product_name = input('Product Name: ').strip()
            if product_name not in products:
                print(f'{product_name} not in cart.')
            if not should_continue():
                break
            else:
                products.remove(product_name)
                print(f'{product_name} removed from cart.')
                if not should_continue():
                    break
        elif request == 3:
            if len(products) <= 0:
                print('Your cart is empty.')
                continue
            for i, item in enumerate(products):
                print(f'{i}: {item}')
            if not should_continue():
                break
        else:
            print('Invalid response, (5) to exit')

if __name__ == '__main__':
    shopping_cart_system()
