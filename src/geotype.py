class GeoType:

    def __init__(self, name: str, driver: str):
        self.name = name
        self.driver = driver

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


SHAPEFILE = GeoType('SHAPEFILE', 'ESRI Shapefile')
MAPINFO = GeoType('MAPINFO', 'MapInfo File')
