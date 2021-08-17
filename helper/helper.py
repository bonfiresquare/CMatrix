from typing import Union

# returns a list with all items being unique without changing the given order
# note that 0 == False and 1 == True, means that if both of them exist, only one of them will be in the output
def unique(input: list) -> list:
    _uli = []
    for item in input:
        _uli.append(item) if item not in _uli else None
    return _uli

# returns a list of keys or values of one or more given dictionaries
# they can also be returned as unique lists (each value is unique in it's own subset but can exist in multiple subsets)
# lists of dictionaries will be return as lists of lists of keys/values; unwrapping them may be useful
def unpair(input: Union[dict, list, tuple], func, _unique) -> Union[dict, list, tuple]:
    if isinstance(input, dict):
        result = list(func(input))
    else:
        result = input.__class__( unpair(item, func, _unique) for item in input if isinstance(item, dict) )
    return unique(result) if _unique else result

# depends on (function) split_dict
# returns a list of keys of the given dictionary
def keys(input: Union[dict, list, tuple], unique = False) -> Union[dict, list, tuple]:
    return unpair(input, dict.keys, unique)

# depends on (function) split_dict
# returns a list of values of the given dictionary
def values(input: Union[dict, list, tuple], unique = False) -> Union[dict, list, tuple]:
    return unpair(input, dict.values, unique)

# returns a subset of items of the given input type
def select(input: Union[dict, list, tuple], selection: list, ):
    if isinstance(input, dict):
        return dict( (key, input[key]) for key in selection if key in input )
    else:
        if len(selection) > 1:
            return input.__class__( input[index] for index in selection if index in range(len(input)) )
        else:
            return input[selection[0]] if selection[0] in range(len(input)) else None

# depends on (function) select
# returns object of the given input type with subselected items from the first level
# works best with a list or tuple of same type/size objects
def subselect(input: Union[list, tuple], selection: list) -> Union[list, tuple]:
    return input.__class__(select(item, selection) for item in input)

# unwraps any nested list and returns all members as list at first level
def unwrap(input: list, output: list) -> list:
    for item in input:
        unwrap(item, output) if isinstance(item, list) else output.append(item)
    return output

# filters a list of dictionaries for specific values and returns them as list
def where(input: Union[list, tuple], property: str, value) -> Union[list, tuple]:
    result = filter(lambda dict: dict[property] == value, input)
    return input.__class__(result)
