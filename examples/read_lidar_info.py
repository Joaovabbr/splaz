#type: ignore
"""
Exemplo: Leitura e exibição de informações de um arquivo LiDAR.

Este script lê um arquivo .laz usando laspy e exibe informações importantes
como número de pontos, bounding box, classes de pontos, etc.
"""
import numpy as np
from splaz import downloader, geocoder

def main():
    dl = downloader.SpLaz()
    geo = geocoder.SpLazGeo(dl)
    try:
        endereco = "Avenida santo amaro, 1826, São Paulo, SP"
        codigo = geo.get_quadrant_by_address(endereco)
        print(f"Código encontrado: {codigo}")
        quadrante = dl.download_quadrante(codigo)
        las_data = quadrante.to_laspy()

        print("\n=== Informações do Arquivo LiDAR ===")
        print(f"Número total de pontos: {len(las_data)}")

        # Bounding box
        min_x, max_x = las_data.x.min(), las_data.x.max()
        min_y, max_y = las_data.y.min(), las_data.y.max()
        min_z, max_z = las_data.z.min(), las_data.z.max()
        print(f"Bounding Box X: {min_x:.2f} a {max_x:.2f}")
        print(f"Bounding Box Y: {min_y:.2f} a {max_y:.2f}")
        print(f"Bounding Box Z: {min_z:.2f} a {max_z:.2f}")

        # Classes de pontos (se disponível)
        if hasattr(las_data, 'classification'):
            unique_classes, counts = np.unique(las_data.classification, return_counts=True)  
            print(f"\nClasses de pontos encontradas:")
            for cls, count in zip(unique_classes, counts):
                print(f"  Classe {cls}: {count} pontos")

        # Intensidade (se disponível)
        if hasattr(las_data, 'intensity'):
            print(f"\nIntensidade média: {las_data.intensity.mean():.2f}")
            print(f"Intensidade mínima: {las_data.intensity.min()}")
            print(f"Intensidade máxima: {las_data.intensity.max()}")

        # Retorno (return number)
        if hasattr(las_data, 'return_number'):
            unique_returns, counts = np.unique(las_data.return_number, return_counts=True)
            print(f"\nNúmeros de retorno:")
            for ret, count in zip(unique_returns, counts):
                print(f"  Retorno {ret}: {count} pontos")

        # Sistema de coordenadas (se disponível no header)
        print(f"\nSistema de coordenadas: EPSG:{las_data.header.parse_crs().to_epsg()}")

    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")

if __name__ == "__main__":
    main()