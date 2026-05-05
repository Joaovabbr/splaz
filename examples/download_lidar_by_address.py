"""
Exemplo: Download de dados LiDAR a partir de um endereço.

Este script geocodifica um endereço, encontra quadrantes LiDAR próximos
e baixa os dados, salvando em data/LiDAR/.
"""

import os
from pathlib import Path
from splaz import downloader, geocoder

def main():
    # Endereço de exemplo
    endereco = "Parque Ibirapuera"

    # Inicializa geocoder e downloader
    dl = downloader.SpLaz()
    geo = geocoder.SpLazGeo(dl)

    print(f"Obtendo código do endereço: {endereco}")
    try:
        #Obter código do quadrante no mesmo sistema de coordenadas do GeoSampa
        codigo = geo.get_quadrant_by_address(endereco)
        print(f"Código encontrado: {codigo}")

        # Cria pasta de destino
        output_dir = Path("data/LiDAR")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Baixando quadrante do GeoSampa
        print(f"Baixando quadrante: {codigo}")
        quadrante = dl.download_quadrante(codigo)
        quadrante.save("data/LiDAR")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()