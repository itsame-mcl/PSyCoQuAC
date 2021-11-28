from typing import Union, Tuple


def int_to_tuple(value: Union[int, Tuple[int]]) -> Tuple[int]:
    if isinstance(value, int):
        tuple_val = (value,)
    else:
        tuple_val = value
    return tuple_val
