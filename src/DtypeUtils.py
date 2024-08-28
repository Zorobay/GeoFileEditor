import re
import typing


class DtypeUtils:
    REG_DTYPE = re.compile(r'(\w+):(\d+).?(\d+)?')

    @classmethod
    def cast_to_dtype(cls, dtype: str, new_val: typing.Any) -> typing.Any:
        if new_val == '' or None:
            return None
        try:
            if dtype == 'int':
                return int(new_val)
            elif cls.is_str_dtype(dtype):
                return str(new_val)
            elif cls.is_float_dtype(dtype):
                num_num, num_dec = cls.get_float_bounds(dtype)
                return round(float(new_val), num_dec)
            else:
                print(f'Warning! Unknown dtype {dtype} for value {new_val}. Using without casting.')
                return new_val
        except ValueError:
            raise CastException('Cast error!')

    @classmethod
    def to_string(cls, dtype: str, value: typing.Any) -> str:
        if value is None:
            return ''
        elif cls.is_float_dtype(dtype):
            num_num, num_dec = cls.get_float_bounds(dtype)
            return str(round(value, num_dec))
        else:
            return str(value)

    @classmethod
    def is_float_dtype(cls, dtype: str) -> bool:
        return dtype.startswith('float:')

    @classmethod
    def is_str_dtype(cls, dtype: str) -> bool:
        return dtype.startswith('str:')

    @classmethod
    def get_float_bounds(cls, dtype: str):
        if match := cls.REG_DTYPE.match(dtype):
            num_num = int(match.group(2)) if match.group(2) else 0
            num_dec = int(match.group(3)) if match.group(3) else 0
            return num_num, num_dec
        else:
            raise Exception(f'Can not extract bounds from unknown dtype {dtype}')


class CastException(RuntimeError):

    def __init__(self, message: str):
        super(RuntimeError, self).__init__(message)
