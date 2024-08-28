import os
import re
import shutil
import typing
import uuid
from pathlib import Path
from zipfile import ZipFile

import fiona
import geopandas

from src.geotype import GeoType, MAPINFO, SHAPEFILE
from src.utils.GeoData import GeoData

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


def read_geo_zip(filepath: str) -> GeoData:
    gdf = geopandas.read_file(filepath, engine='fiona')
    with fiona.open(f'zip://{filepath}') as f:
        schema = f.schema
    return GeoData(gdf, schema)


def write_new_zip(data: GeoData, filepath: str, geo_type: GeoType):
    try:
        data.write_to_file(filepath, geo_type)
        archive_name = shutil.make_archive(str(filepath), 'zip', str(filepath))
        shutil.rmtree(filepath)
        print(f'Done writing archive {archive_name}')
    except Exception as e:
        print(e)


def overwrite_zip(gdf: GeoData, filepath: str, geo_type: GeoType):
    filepath = Path(filepath)
    temp_folder = str(uuid.uuid4())
    temp_archive_name = str(uuid.uuid4())
    temp_path = filepath.parent / temp_folder

    print(f'Writing to temp. directory {temp_path} with type {geo_type.name}')
    gdf.write_to_file(str(temp_path), geo_type)
    print(f'Creating archive {temp_folder}.zip')
    archive_name = shutil.make_archive(str(temp_archive_name), 'zip', str(temp_path))
    print(f'Removing old archive {filepath}')
    os.remove(filepath)
    print(f'Renaming archive {Path(archive_name).name} -> {filepath.name}')
    os.rename(archive_name, filepath)
    print(f'Done overwriting archive {filepath}')
    shutil.rmtree(temp_path)
    print(f'Removed temp file {temp_path}')
