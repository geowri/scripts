#!/usr/bin/env python3
import os
import sys
import fiona
from osgeo import gdal, ogr

# Habilitar exceções no GDAL
gdal.UseExceptions()

def cortar_raster_com_shapefile(raster_path, shapefile_path, output_path):
    """
    Corta um arquivo raster com um shapefile.

    Parâmetros:
    raster_path (str): Caminho para o arquivo raster (.tif).
    shapefile_path (str): Caminho para o shapefile (.shp).
    output_path (str): Caminho para salvar o arquivo raster cortado.

    Retorno:
    None. O arquivo cortado será salvo no local especificado.
    """
    # Abrir o shapefile e obter a geometria
    with fiona.open(shapefile_path, 'r') as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]

    # Abrir o raster
    raster = gdal.Open(raster_path)

    # Definir o driver GeoTIFF
    driver = gdal.GetDriverByName('GTiff')

    # Criar o recorte utilizando o shapefile
    options = gdal.WarpOptions(
        format="GTiff", cutlineDSName=shapefile_path, cropToCutline=True
    )
    print(f"INFO: Cortando o raster {raster_path} com o shapefile {shapefile_path}...")

    # Executar o corte
    gdal.Warp(output_path, raster, options=options)

    print(f"INFO: Raster cortado salvo como {output_path}.")

# Função principal para capturar os argumentos da linha de comando
def main():
    if len(sys.argv) != 4:
        print("Uso correto: python cortar_raster_com_shapefile.py raster.tif shapefile.shp output_cortado.tif")
        sys.exit(1)

    raster_path = sys.argv[1]
    shapefile_path = sys.argv[2]
    output_path = sys.argv[3]

    try:
        cortar_raster_com_shapefile(raster_path, shapefile_path, output_path)
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()

