import pytest
import io
import zipfile
from splaz.downloader import SpLaz
from splaz.entities import LidarQuadrante
from splaz.constants import GEOSAMPA_DOWNLOAD_URL


@pytest.fixture
def client():
    return SpLaz()

@pytest.fixture
def fake_zip_content():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf,"w") as z:
        z.writestr("3316-153.laz", b"fake_laz_binary_content")
    return buf.getvalue()

def test_download_quadrante_sucesso(client, requests_mock, fake_zip_content):
    requests_mock.get(GEOSAMPA_DOWNLOAD_URL, content=fake_zip_content, status_code = 200)

    resultado = client.download_quadrante("3316-153")

    assert isinstance(resultado,LidarQuadrante)
    assert resultado.codigo == "3316-153"
    assert resultado.esta_carregado is True
    assert resultado.conteudo_binario == b"fake_laz_binary_content"


def test_download_quadrante_erro_404(client,requests_mock):
    requests_mock.get(GEOSAMPA_DOWNLOAD_URL, status_code = 404 )
    import requests

    with pytest.raises(ValueError):
        client.download_quadrante("codigo-inexistente")

def test_processar_zip_invalido(client):
    codigo = "test"
    with pytest.raises(ValueError, match= f"Conteudo baixado para o quadrante {codigo} invalido."):
        client._processar_zip(codigo, b"not_a_zip_file")

def test_download_lista_chama_multiplos(client, requests_mock, fake_zip_content):
    requests_mock.get(GEOSAMPA_DOWNLOAD_URL, content=fake_zip_content)
    
    codigos = ["1111-111", "2222-222"]
    resultados = client.download_lista(codigos)

    assert len(resultados) == 2
    assert requests_mock.call_count == 2
