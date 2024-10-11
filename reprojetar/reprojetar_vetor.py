#!/usr/bin/env python3
import geopandas as gpd
from pyproj import CRS
import argparse
import sys

def get_common_projections():
    """
    Retorna um dicionário com algumas projeções comuns e seus códigos EPSG.
    """
    return {
        'WGS84': 'EPSG:4326',
        'Mercator': 'EPSG:3857',
        'SIRGAS 2000 / UTM zone 23S': 'EPSG:31983',
        'SIRGAS 2000 / UTM zone 24S': 'EPSG:31984',
        'South America Albers Equal Area Conic': 'ESRI:102033',
    }

def list_projections():
    """
    Lista projeções comuns que podem ser usadas.
    """
    print("Projeções comuns disponíveis:")
    for name, epsg in get_common_projections().items():
        print(f"  - {name}: {epsg}")

def reprojetar_vetor(input_vector, output_vector, target_crs):
    """
    Reprojeta um arquivo vetorial (shapefile, GeoJSON, etc.) para uma projeção especificada.

    Parâmetros:
    - input_vector (str): Caminho para o arquivo vetorial de entrada.
    - output_vector (str): Caminho para o arquivo vetorial de saída reprojetado.
    - target_crs (str): Código EPSG ou proj4 da projeção de destino.
    """
    try:
        # Carrega o arquivo vetorial original
        gdf = gpd.read_file(input_vector)

        # Verifica se o arquivo vetorial possui um CRS definido
        if gdf.crs is None:
            print("Erro: O arquivo vetorial de entrada não possui um sistema de coordenadas definido.")
            sys.exit(1)

        # Mostra o CRS original
        original_crs = gdf.crs
        print(f"Projeção original: {original_crs}")

        # Reprojeta para o CRS alvo
        gdf_reprojetado = gdf.to_crs(target_crs)

        # Mostra o CRS alvo
        target_crs_info = CRS(target_crs)
        print(f"Projeção após reprojeção: {target_crs_info}")

        # Salva o arquivo vetorial reprojetado
        gdf_reprojetado.to_file(output_vector)
        print(f"Arquivo vetorial reprojetado salvo como: {output_vector}")

    except Exception as e:
        print(f"Erro ao reprojetar o arquivo vetorial: {e}")
        sys.exit(1)

def main():
    # Configurando o parser de argumentos
    parser = argparse.ArgumentParser(
        description="Reprojetar arquivos vetoriais (shapefile, GeoJSON, etc.) para uma projeção específica.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_vector", nargs='?', help="Caminho para o arquivo vetorial de entrada")
    parser.add_argument("output_vector", nargs='?', help="Caminho para o arquivo vetorial de saída")
    parser.add_argument("target_crs", nargs='?', help=(
        "Código EPSG ou proj4 da projeção alvo.\n"
        "Exemplos de códigos EPSG: 'EPSG:4326', 'EPSG:3857'\n"
        "Use '--list' para ver projeções comuns."
    ))
    parser.add_argument("--list", action="store_true", help="Lista projeções comuns disponíveis")

    args = parser.parse_args()

    if args.list:
        list_projections()
        sys.exit(0)  # Sucesso ao listar projeções

    if not args.input_vector or not args.output_vector or not args.target_crs:
        print("Erro: Você deve especificar o input_vector, output_vector e target_crs ou usar a opção '--list' para ver projeções disponíveis.")
        sys.exit(1)

    # Chama a função de reprojeção com os argumentos fornecidos
    reprojetar_vetor(args.input_vector, args.output_vector, args.target_crs)

if __name__ == "__main__":
    main()
