import os
import re
import shutil
import typing
import uuid
from pathlib import Path
from zipfile import ZipFile

import geopandas
from geopandas import GeoDataFrame

from src.geotype import GeoType, MAPINFO, SHAPEFILE

REG_TAB_FILE = re.compile(r'\w+\.tab')
REG_SHP_FILE = re.compile(r'\w+\.shp')


def decide_geo_type(filepath: str) -> GeoType:
    filelist = read_zip_filelist(filepath)
    for file in filelist:
        if Path(file).suffix == '.tab':
            return MAPINFO
        elif Path(file).suffix == '.shp':
            return SHAPEFILE
    raise Exception(f"Can't decide Geo Type from filelist: {filelist}")


def read_zip_filelist(filepath: str) -> typing.List[str]:
    with ZipFile(filepath) as f:
        return f.namelist()


def read_geo_zip(filepath: str) -> GeoDataFrame:
    return geopandas.read_file(filepath)


def write_new_zip(gdf: GeoDataFrame, filepath: str, geo_type: GeoType):
    try:
        gdf.to_file(filepath, driver=geo_type.driver)
        archive_name = shutil.make_archive(str(filepath), 'zip', str(filepath))
        shutil.rmtree(filepath)
        print(f'Done writing archive {archive_name}')
    except Exception as e:
        print(e)


def overwrite_zip(gdf: GeoDataFrame, filepath: str, geo_type: GeoType):
    filepath = Path(filepath)
    temp_folder = str(uuid.uuid4())
    temp_archive_name = str(uuid.uuid4())
    temp_path = filepath.parent / temp_folder

    gdf.to_file(str(temp_path), driver=geo_type.driver)
    print(f'Writing to temp. directory {temp_path} with type {geo_type.name}')
    archive_name = shutil.make_archive(str(temp_archive_name), 'zip', str(temp_path))
    print(f'Creating archive {temp_folder}.zip')
    os.remove(filepath)
    print(f'Removing old archive {filepath}')
    os.rename(archive_name, filepath)
    print(f'Renaming archive {Path(archive_name).name} -> {filepath.name}')
    shutil.rmtree(temp_path)
    print(f'Done overwriting archive {filepath}')
