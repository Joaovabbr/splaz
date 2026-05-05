[![Python Tests](https://github.com/Joaovabbr/splaz/actions/workflows/tests.yml/badge.svg)](https://github.com/Joaovabbr/splaz/actions/workflows/tests.yml)
[![PyPI version](https://img.shields.io/pypi/v/splaz.svg)](https://pypi.org/project/splaz/)
[![Python versions](https://img.shields.io/pypi/pyversions/splaz.svg)](https://pypi.org/project/splaz/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# SpLaz (Vagas Verdes)
A SpLaz é uma biblioteca Python de alto nível projetada para automatizar a obtenção de dados LiDAR (nuvens de pontos) da cidade de São Paulo via portal GeoSampa. Ela resolve complexidades de geocodificação, conversão de sistemas de coordenadas (SIRGAS 2000 / UTM 23S) e instabilidades de download de servidores legados.

Este projeto é a base técnica do projeto Vagas Verdes, focado em identificar áreas potenciais para arborização urbana utilizando sensoriamento remoto.

## 🚀 Funcionalidades
- Geocodificação por Endereço: Identifica automaticamente qual quadrante LiDAR baixar a partir de um endereço textual (ex: "Rua Quatá, 300").

- Busca por Bairro: Lista e baixa todos os quadrantes que compõem um bairro específico.

- Tratamento de Dados Espaciais: Download e extração automática da grade de articulação (Shapefile) da prefeitura.

- Resiliência de Rede: Sistema de correção de encoding (ISO-8859-1) e verificação de integridade de arquivos ZIP.

- Gestão de Cache: Armazenamento inteligente na pasta local .geosp_laz_api para evitar downloads repetitivos e poupar banda.

## 📦 Instalação

``` Bash
pip install splaz
```
### 🛠 Exemplos de Uso
#### 1. Configuração Inicial
```Python

from splaz import SpLaz, SpLazGeo

client = SpLaz()
geo = SpLazGeo(client=client)
```
#### 2. Download por Código do Quadrante
Ideal quando você já possui o mapeamento da grade de 2020:

```Python

quadrante = client.download_quadrante("3316-153")
quadrante.save("data/raw/laz")
```
#### 3. Download por Endereço (Geocodificação)
A forma mais intuitiva de acessar os dados para um local específico:

```Python

endereco = "Avenida Santo Amaro, 1826"
codigo = geo.get_quadrant_by_address(endereco)
print(f"Quadrante identificado: {codigo}")
client.download_quadrante(codigo).save("data/raw/laz")
```
#### 4. Download por Coordenadas (Lat/Lon)
Para integração com GPS ou outros sistemas de mapeamento:

```Python

lat, lon = -23.598, -46.676
codigo = geo.get_quadrant_by_coords(lat, lon)
client.download_quadrante(codigo).save("data/raw/laz")
```
#### 5. Processamento por Bairro
Obtenha todos os quadrantes que interceptam a área de um bairro:

```Python

bairro = "Itaim Bibi"
codigos = geo.get_quadrants_by_neighborhood(bairro)

for cod in codigos:
    client.download_quadrante(cod).save(f"data/raw/laz/{bairro}")
```
#### 6. Manipulando a Classe LidarQuadrante
A classe abstrai a complexidade dos binários baixados:

```Python

quadrante = client.download_quadrante("3316-153")

# Atributos úteis
print(quadrante.codigo)             # "3316-153"
print(quadrante.esta_carregado)     # True
print(len(quadrante.conteudo_binario)) # Tamanho em bytes do arquivo .laz

# Salva o arquivo final no disco
quadrante.save(dest_path="output/lidar")
```
## 📂 Estrutura do Projeto
```Plaintext

src/splaz/
├── entities.py    # Representação de objetos LiDAR
├── downloader.py  # Lógica de comunicação com GeoSampa
├── geocoder.py    # Cálculos espaciais e geolocalização
└── constants.py   # EPSG, URLs e parâmetros de API
```
## 🧪 Testes Automatizados
A biblioteca possui uma suíte de testes robusta (Unitários, Integração e E2E) que valida desde a lógica de coordenadas até o download real. Para rodar:

```Bash
pytest
```

### 📄 Licença
Distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
### 🎓 Contexto Acadêmico
Este projeto foi desenvolvido como parte de um projeto de Iniciação Científica no Insper.

Autor: João Braga

Perfil: Aluno do 7° semestre de Engenharia da Computação.

Objetivo: Apoiar a análise de dados geoespaciais para o projeto ambiental "Vagas Verdes".
