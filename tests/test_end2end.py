import pytest
from splaz import SpLazGeo, SpLaz

def test_fluxo_completo_insper_vagas_verdes():
    """
    TESTE DE SISTEMA (E2E):
    Valida se a biblioteca consegue converter um endereço real,
    identificar o quadrante e baixar o arquivo binário sem erros.
    """
    # 1. Inicialização (Sem mocks!)
    client = SpLaz()
    geo = SpLazGeo(client=client)
    
    # Endereço real do Insper
    endereco = "Avenida Santo Amaro, 1826"
    
    # 2. Execução do fluxo
    # O Geocoder deve baixar a grade automaticamente no primeiro uso
    codigo_quadrante = geo.get_quadrant_by_address(endereco)
    
    # 3. Verificação do Geocoding
    # Sabemos que o Insper fica no quadrante 3316-153
    assert codigo_quadrante == "3316-153"
    
    # 4. Download Real
    # Baixamos apenas um para não sobrecarregar sua rede
    quadrante_obj = client.download_quadrante(codigo_quadrante)
    
    # 5. Verificações Finais
    assert quadrante_obj.esta_carregado is True
    assert len(quadrante_obj.conteudo_binario) > 0
    assert quadrante_obj.nome_arquivo.endswith(".laz")
    
    print(f"\n[E2E] Sucesso: Quadrante {codigo_quadrante} baixado com {len(quadrante_obj.conteudo_binario)} bytes.")