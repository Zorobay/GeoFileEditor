import os
import shutil
import uuid
from pathlib import Path

import geopandas
from geopandas import GeoDataFrame


def read_geo_zip(filepath: str) -> GeoDataFrame:
    return geopandas.read_file(filepath)


def write_new_zip(gdf: GeoDataFrame, filepath: str):
    try:
        gdf.to_file(filepath, driver='ESRI Shapefile')
        archive_name = shutil.make_archive(str(filepath), 'zip', str(filepath))
        shutil.rmtree(filepath)
        print(f'Done writing archive {archive_name}')
    except Exception as e:
        print(e)

def overwrite_zip(gdf: GeoDataFrame, filepath: str):
    try:
        filepath = Path(filepath)
        temp_folder = str(uuid.uuid4())
        temp_archive_name = str(uuid.uuid4())
        temp_path = filepath.parent / temp_folder

        gdf.to_file(str(temp_path), driver='ESRI Shapefile')
        print(f'Writing to temp. directory {temp_path}')
        archive_name = shutil.make_archive(str(temp_archive_name), 'zip', str(temp_path))
        print(f'Creating archive {temp_folder}.zip')
        os.remove(filepath)
        print(f'Removing old archive {filepath}')
        os.rename(archive_name, filepath)
        print(f'Renaming archive {Path(archive_name).name} -> {filepath.name}')
        shutil.rmtree(temp_path)
        print(f'Done overwriting archive {filepath}')
    except Exception as e:
        print(e)
