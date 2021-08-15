from typing import Union

# returns a subset of items of the given input type
def select(input: Union[dict, list, tuple], selection: list):
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
def subselect(input: Union[list, tuple], selection: list):
    return input.__class__(select(item, selection) for item in input)
