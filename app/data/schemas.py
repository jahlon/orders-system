def product_schema(product) -> dict:
    return {
        'id': str(product['_id']),
        'name': product["name"],
        'sku': product['sku'],
        'price': product['price'],
        'description': product['description'],
        'image': product['image']
    }


def order_schema(order) -> dict:
    return {
        'id': str(order['_id']),
        'products': order['products'],
        'total': order['total'],
        'status': order['status'],
        'created_at': order['created_at'],
        'updated_at': order['updated_at']
    }
