#!/usr/bin/env python3
import geopandas as gpd
from pyproj import CRS
import argparse

def reprojetar_shapefile(input_shapefile, output_shapefile, target_crs):
    # Carrega o shapefile original
    gdf = gpd.read_file(input_shapefile)

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

if __name__ == "__main__":
    # Configurando o parser de argumentos
    parser = argparse.ArgumentParser(description="Reprojetar shapefile para uma projeção específica.")
    parser.add_argument("input_shapefile", help="Caminho para o shapefile de entrada")
    parser.add_argument("output_shapefile", help="Caminho para o shapefile de saída")
    parser.add_argument("target_crs", help="Código EPSG da projeção alvo")

    args = parser.parse_args()

    # Chama a função de reprojeção com os argumentos fornecidos
    reprojetar_shapefile(args.input_shapefile, args.output_shapefile, args.target_crs)
