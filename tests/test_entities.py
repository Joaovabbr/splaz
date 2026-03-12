import pytest
import os
from splaz.entities import LidarQuadrante

def test_lidar_quadrante_inicializacao_vazia():
    quad = LidarQuadrante("3316-153")
    assert quad.codigo == "3316-153"
    assert quad.esta_carregado is False
    assert "Vazio" in repr(quad)

def test_lidar_quadrante_inicializa_com_dados():
    dados_falsos = b"LAZ_BINARY_DATA"
    quad = LidarQuadrante(codigo="3316-153", conteudo_binario=dados_falsos, nome_arquivo="3316-153.laz")

    assert quad.esta_carregado is True
    assert quad.conteudo_binario == dados_falsos
    assert "Carregado" in repr(quad)

def test_save_com_sucesso(tmp_path):
    d = tmp_path / "data_test"
    d.mkdir()
    nome_arq = "test_vagas_verdes.laz"
    dados = b"01010101"

    quad = LidarQuadrante("3316-153", dados, nome_arq)
    caminho_salvo = quad.save(str(d))

    assert os.path.exists(caminho_salvo)
    with open(caminho_salvo, "rb") as f:
        assert f.read() == dados

def test_save_sem_dados_levanta_erro():
    codigo = "3316-153" 
    quad = LidarQuadrante(codigo)
    with pytest.raises(ValueError, match=f"O quadrante {codigo} não possui dados em memória."):
        quad.save("pasta_qualquer")

