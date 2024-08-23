from db import initiate_db, get_all_products

def get_products_list():
    initiate_db()
    products = get_all_products()
    product_list = []
    for product in products:
        product_list.append(f"Название: {product[0]} | Описание: {product[1]} | Цена: {product[2]}")
    return product_list
