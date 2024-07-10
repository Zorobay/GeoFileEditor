import typing


class DtypeUtils:

    @classmethod
    def cast_to_dtype(cls, dtype: str, new_val: typing.Any) -> typing.Any:
        if new_val == '':
            return None
        try:
            if dtype == 'int':
                return int(new_val)
            elif dtype.startswith('str:'):
                return str(new_val)
            elif dtype.startswith('float:'):
                return float(new_val)
            else:
                print(f'Warning! Unknown dtype {dtype} for value {new_val}. Using without casting.')
                return new_val
        except ValueError:
            raise CastException('Cast error!')


class CastException(RuntimeError):

    def __init__(self, message: str):
        super(RuntimeError, self).__init__(message)
