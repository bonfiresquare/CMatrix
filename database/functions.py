from helper import intersect, join
import database.Database as db

def validate_str(fields: dict) -> dict:
	return {k:str(v).replace("'","''") if v.__class__ in [str, dict, list, tuple] else v for k,v in fields.items()}

def strip(table: str, fields: dict) -> dict:
	columns = db.Database._columns[table]
	if intersect(fields.keys(), columns, test=True):
		return {k:v for k,v in fields.items() if k.lower() in columns}
	else:
		return fields

def condition(conditions: dict, operator: str = 'AND'):
	# allowed operators: AND, OR
	if len(conditions):
		return ' WHERE ' + join(list(f'"{k}" = "{v}"' for k,v in conditions.items()), f' {operator} ')
	else:
		return ''

def select(table: str, fields: str = '*', conditions: dict = {}):
	query = f'SELECT "{fields}" FROM "{table}"'
	query += condition(conditions)
	data = db.Database.exec(query)
	return data

def insert(table: str, fields: dict, *,commit: bool = False):
	fields = strip(table, fields)
	fields = validate_str(fields)
	query = f'INSERT INTO "{table}" ('
	query += join(fields.keys(),wrap='""')
	query += ') VALUES ('
	query += join(fields.values(),wrap="''")
	query += ')'
	db.Database.exec(query, commit=commit)
	return

def update(table: str, fields: dict, conditions: dict = {}, *, commit: bool = False):
	fields = strip(table, fields)
	fields = validate_str(fields)
	query = f'UPDATE {table} SET '
	query += join(list(f'"{key}" = "{fields[key]}"' for key in fields.keys()))
	query += condition(conditions)
	db.Database.exec(query, commit=commit)
	return
