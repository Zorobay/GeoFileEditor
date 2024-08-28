import typing

from geopandas import GeoDataFrame

from src.DtypeUtils import DtypeUtils, CastException
from src.geotype import GeoType
from src.gui import toasts


class GeoData:

    def __init__(self, gdf: GeoDataFrame, schema: dict):
        self._gdf = gdf
        self._full_schema = schema
        self._schema = schema['properties']
        self._original_attrs = self._extract_data_attrs()

    def get_value(self, feature_index: int, attribute: str) -> typing.Any:
        return self._gdf.loc[feature_index, attribute]

    def set_value(self, feature_index: int, attribute: str, value: typing.Any):
        old_val = self.get_value(feature_index, attribute)
        new_val = self._cast_to_dtype(attribute, value, old_val)
        self._gdf.loc[feature_index, attribute] = new_val

    def get_original_value(self, feature_index: int, attribute: str) -> typing.Any:
        return self._original_attrs[feature_index][attribute]

    def schema(self) -> dict:
        return self._schema

    def num_features(self):
        return len(self._gdf)

    def write_to_file(self, filepath: str, geo_type: GeoType):
        self._gdf.to_file(filepath, schema=self._full_schema, engine='fiona', driver=geo_type.driver)

    def update_original_attrs(self):
        self._original_attrs = self._extract_data_attrs()

    def _extract_data_attrs(self) -> typing.List[dict]:
        out = []
        for i in range(self._gdf.shape[0]):
            out.append(dict(self._gdf.loc[i, :]))

        return out

    def _cast_to_dtype(self, key: str, new_val, old_val) -> typing.Any:
        dtype = self._schema[key]
        try:
            return DtypeUtils.cast_to_dtype(dtype, new_val)
        except CastException as e:
            toasts.error_toast('Cast exception!',
                               f'Field <strong>{key}</strong> with value {new_val} can not be cast to type {dtype}. Reverting to old value {old_val}!')

        return old_val
