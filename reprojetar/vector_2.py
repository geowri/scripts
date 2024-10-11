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

def reprojetar_shapefile(input_shapefile, output_shapefile, target_crs):
    """
    Reprojeta um shapefile para uma projeção especificada.

    Parâmetros:
    - input_shapefile (str): Caminho para o shapefile de entrada.
    - output_shapefile (str): Caminho para o shapefile de saída reprojetado.
    - target_crs (str): Código EPSG ou proj4 da projeção de destino.
    """
    try:
        # Carrega o shapefile original
        gdf = gpd.read_file(input_shapefile)

        # Verifica se o shapefile possui um CRS definido
        if gdf.crs is None:
            print("Erro: O shapefile de entrada não possui um sistema de coordenadas definido.")
            sys.exit(1)

        # Mostra o CRS original
        original_crs = gdf.crs
        print(f"Projeção original: {original_crs}")

        # Reprojeta para o CRS alvo
        gdf_reprojetado = gdf.to_crs(target_crs)

        # Mostra o CRS alvo
        target_crs_info = CRS(target_crs)
        print(f"Projeção após reprojeção: {target_crs_info}")

        # Salva o shapefile reprojetado
        gdf_reprojetado.to_file(output_shapefile)
        print(f"Shapefile reprojetado salvo como: {output_shapefile}")

    except Exception as e:
        print(f"Erro ao reprojetar o shapefile: {e}")
        sys.exit(1)

def main():
    # Configurando o parser de argumentos
    parser = argparse.ArgumentParser(
        description="Reprojetar shapefile para uma projeção específica.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_shapefile", nargs='?', help="Caminho para o shapefile de entrada")
    parser.add_argument("output_shapefile", nargs='?', help="Caminho para o shapefile de saída")
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

    if not args.input_shapefile or not args.output_shapefile or not args.target_crs:
        print("Erro: Você deve especificar o input_shapefile, output_shapefile e target_crs ou usar a opção '--list' para ver projeções disponíveis.")
        sys.exit(1)

    # Chama a função de reprojeção com os argumentos fornecidos
    reprojetar_shapefile(args.input_shapefile, args.output_shapefile, args.target_crs)

if __name__ == "__main__":
    main()

