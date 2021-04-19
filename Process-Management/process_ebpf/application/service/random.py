import uuid

def get_random():
    order_number = str(uuid.uuid1()).upper().replace('-','')
    return order_number
