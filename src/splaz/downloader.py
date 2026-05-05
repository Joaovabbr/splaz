import requests
import zipfile
import io
from importlib.resources import files
from .entities import LidarQuadrante
from .constants import (
    GEOSAMPA_DOWNLOAD_URL,
    LAZ_DOWNLOAD_PARAMS,
)

class SpLaz:
    """
    Cliente para acessar e baixar dados LIDAR do portal GeoSampa.
    Gerencia a grade de articulação e o download de quadrantes específicos.
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        # Carrega o shapefile do grid embarcado na biblioteca
        self.grid_path = self._obter_caminho_grid()

    def _obter_caminho_grid(self) -> str:
        """Obtém o caminho do arquivo shapefile do grid embarcado na biblioteca."""
        try:
            # Acessa o arquivo de dados embarcado na biblioteca
            data_path = files('splaz').joinpath('data')
            shp_files = list(data_path.glob('*.shp')) #type: ignore
            if not shp_files:
                raise FileNotFoundError("Nenhum arquivo .shp encontrado em splaz/data/")
            return str(shp_files[0])
        except Exception as e:
            raise FileNotFoundError(f"Erro ao localizar grid embarcado: {e}")

    def download_quadrante(self, codigo_quadra: str) -> LidarQuadrante:
        """
        Baixa um quadrante LIDAR específico do GeoSampa.

        Args:
            codigo_quadra (str): Código do quadrante a ser baixado.

        Returns:
            LidarQuadrante: Objeto contendo os dados do quadrante baixado.
        """
        params = {
            "orig": LAZ_DOWNLOAD_PARAMS["orig"],
            "arq": f"{LAZ_DOWNLOAD_PARAMS['arq']}\\{codigo_quadra}.zip",
            "arqTipo": LAZ_DOWNLOAD_PARAMS["arq_tipo"]
        }

        response = self.session.get(GEOSAMPA_DOWNLOAD_URL, params=params, timeout=30)

        return self._processar_zip(codigo_quadra, response.content)

    def _processar_zip(self, codigo: str, conteudo_zip: bytes) -> LidarQuadrante:
        try:
            with zipfile.ZipFile(io.BytesIO(conteudo_zip)) as z:
                nome_laz = z.namelist()[0]
                dados_laz = z.read(nome_laz)
                return LidarQuadrante(codigo, dados_laz, nome_laz)
        except zipfile.BadZipFile:
            raise ValueError(f"Conteudo baixado para o quadrante {codigo} invalido.")

    def download_lista(self, codigos: list) -> list:
        return [self.download_quadrante(c) for c in codigos]