import geopandas as gpd
from geopy.geocoders import Nominatim
from shapely.geometry import Point, box
from .constants import EPSG_SAO_PAULO
from .downloader import SpLaz

class SpLazGeo:
    """
    Gerenciador de geocodificação para dados LIDAR do GeoSampa.
    """
    def __init__(self, client: SpLaz | None = None):
        self.client = client or SpLaz()
        self._grid = None
        self.geolocator = Nominatim(user_agent="geosp_laz_api_vagas_verdes")
    @property
    def grid(self) -> gpd.GeoDataFrame:
        """
        Carrega e prepara o Shapefile de articulação automaticamente.
        Mantém os dados em memória para buscas rápidas.
        """
        if self._grid is None:
            gdf = gpd.read_file(self.client.grid_path)
            
            if gdf.crs is None:
                gdf = gdf.set_crs(epsg=EPSG_SAO_PAULO)
            elif gdf.crs.to_epsg() != EPSG_SAO_PAULO:
                gdf = gdf.to_crs(epsg=EPSG_SAO_PAULO)
            
            self._grid = gdf
        return self._grid

    def get_quadrant_by_coords(self, lat: float, lon: float) -> str:
        """
        Determina o quadrante LIDAR correspondente a coordenadas geográficas.
        Args:
            lat (float): Latitude em graus decimais.
            lon (float): Longitude em graus decimais.
        Returns:
            str: Código do quadrante LIDAR correspondente.
        """
        ponto_gps = gpd.GeoSeries([Point(lon, lat)], crs="EPSG:4326")
        ponto_sp = ponto_gps.to_crs(epsg=EPSG_SAO_PAULO).iloc[0]
        resultado = self.grid[self.grid.contains(ponto_sp)] #type: ignore
        if resultado.empty:
            raise ValueError(f"Coordenadas ({lat}, {lon}) fora da cobertura de SP.")
        print(resultado.columns)
        return str(resultado.iloc[0]['cd_quadric'])

    def get_quadrant_by_address(self, address: str) -> str:
        """
        Determina o quadrante LIDAR correspondente a um endereço.
        Args:
            address (str): Endereço completo ou parcial em São Paulo.
        Returns:
            str: Código do quadrante LIDAR correspondente.
        """
        search_query = f"{address}, São Paulo, SP, Brazil"
        location = self.geolocator.geocode(search_query)
        if not location:
            raise ValueError(f"Endereço não localizado: {address}")
        return self.get_quadrant_by_coords(location.latitude, location.longitude) #type: ignore

    def get_quadrants_by_neighborhood(self, neighborhood: str) -> list[str]:
        """
        Retorna uma lista de quadrantes LIDAR que intersectam um bairro específico.
        Args:
            neighborhood (str): Nome do bairro em São Paulo.
        Returns:
            list[str]: Lista de códigos de quadrantes LIDAR que intersectam o bairro.
        """
        query = f"{neighborhood}, São Paulo, SP, Brazil"
        location = self.geolocator.geocode(query)
        if not location:
            raise ValueError(f"Bairro não encontrado: {neighborhood}")

        bbox = location.raw['boundingbox'] # type: ignore
        lat_min, lat_max, lon_min, lon_max = float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])
        
        area_gps = gpd.GeoSeries([box(lon_min, lat_min, lon_max, lat_max)], crs="EPSG:4326")
        area_sp = area_gps.to_crs(epsg=EPSG_SAO_PAULO).iloc[0]

        intersecao = self.grid[self.grid.intersects(area_sp)] #type: ignore
        
        return intersecao['cd_quadric'].unique().tolist()