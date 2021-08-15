import database.Database as db

def get_coins(field = '*', filter_field = None, filter_value = None):

    query = f'SELECT {field} FROM Coin'
    if filter_field and filter_value:
        query += f' WHERE {filter_field} = {filter_value}'
    data = db.Database.exec(query)
    return data
