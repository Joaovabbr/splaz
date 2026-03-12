import pytest
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon, box
from unittest.mock import MagicMock, patch
from splaz.geocoder import SpLazGeo


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.ensure_grid_data.return_value = "caminho/falso/grade.shp"
    return  client

@pytest.fixture
def mock_grid_gdf():
    """Cria um GeoDataFrame minúsculo para simular a grade de SP."""
    # Quadrado simples representando um quadrante fictício
    poly = Polygon([(0, 0), (1000, 0), (1000, 1000), (0, 1000)])
    gdf = gpd.GeoDataFrame(
        {'qmdt_cod': ['3316-153'], 'geometry': [poly]},
        crs="EPSG:31983"
    )
    return gdf


def test_get_quadrant_by_coords_sucesso(mock_client, mock_grid_gdf):
    with patch("geopandas.read_file", return_value = mock_grid_gdf):
        geo = SpLazGeo(client=mock_client)

        with patch.object(gpd.GeoSeries, "to_crs") as mock_to_crs:
            mock_to_crs.return_value = gpd.GeoSeries([Point(500,500)])

            codigo = geo.get_quadrant_by_coords(-23.5,-46.6)
            assert codigo == '3316-153'

def test_get_quadrant_by_address_sucesso(mock_client, mock_grid_gdf):
    with patch("geopandas.read_file", return_value=mock_grid_gdf):
        geo = SpLazGeo(client=mock_client)
        
        # Mock do retorno do Nominatim (Geopy)
        mock_location = MagicMock()
        mock_location.latitude = -23.59
        mock_location.longitude = -46.67
        
        with patch.object(geo.geolocator, "geocode", return_value=mock_location):
            with patch.object(geo, "get_quadrant_by_coords", return_value="3316-153"):
                codigo = geo.get_quadrant_by_address("Rua Quatá, 300")
                assert codigo == "3316-153"

def test_get_quadrants_by_neighborhood_bbox(mock_client,mock_grid_gdf):
    with patch("geopandas.read_file", return_value=mock_grid_gdf):
        geo = SpLazGeo(client=mock_client)
        
        # 1. Simula o retorno do Nominatim (Bairro real)
        mock_location = MagicMock()
        mock_location.raw = {
            'boundingbox': ['-23.6', '-23.5', '-46.7', '-46.6']
        }
        
        with patch.object(geo.geolocator, "geocode", return_value=mock_location):
            # 2. Mockamos a conversão de coordenadas para que a área resultante
            # coincida com o nosso quadrante de teste (0 a 1000)
            with patch.object(gpd.GeoSeries, "to_crs") as mock_to_crs:
                # Criamos um polígono que sobrepõe o nosso mock_grid_gdf (0,0 a 1000,1000)
                overlap_box = box(100, 100, 500, 500)
                mock_to_crs.return_value = gpd.GeoSeries([overlap_box])
                
                quadrantes = geo.get_quadrants_by_neighborhood("Vila Olímpia")
                
                # Agora deve funcionar, pois as geometrias se interceptam!
                assert isinstance(quadrantes, list)
                assert "3316-153" in quadrantes