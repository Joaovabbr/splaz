import pytest
from splaz.downloader import SpLaz
from splaz.entities import LidarQuadrante



def test_conexao_quadrante():
    """Testa conexão real para download de um quadrante LIDAR."""
    client = SpLaz()
    
    # Use um código de quadrante que você sabe que existe (ajuste conforme necessário)
    codigo_teste = "3316-153"  # Exemplo; substitua por um válido se este não funcionar
    
    try:
        quadrante = client.download_quadrante(codigo_teste)
        assert isinstance(quadrante, LidarQuadrante)
        assert quadrante.codigo == codigo_teste
        assert quadrante.esta_carregado is True
        print(f"Quadrante {codigo_teste} baixado com sucesso")
    except Exception as e:
        pytest.fail(f"Falha no download do quadrante {codigo_teste}: {e}")