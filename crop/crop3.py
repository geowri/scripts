#!/usr/bin/env python3
import sys
import geopandas as gpd
import rasterio
from rasterio.mask import mask

def recortar_raster_com_shapefile(raster_path, shapefile_path, output_raster_path):
    """
    Recorta um arquivo raster com base em um shapefile.

    Parâmetros:
    raster_path (str): Caminho para o arquivo raster (.tif).
    shapefile_path (str): Caminho para o arquivo shapefile (.shp).
    output_raster_path (str): Caminho para salvar o arquivo raster recortado (.tif).

    Retorno:
    str: Caminho para o arquivo raster recortado.
    """
    # Carregar o shapefile
    brasil_shp = gpd.read_file(shapefile_path)
    
    # Abrir o raster original
    with rasterio.open(raster_path) as src:
        # Verificar se o shapefile e o raster estão no mesmo sistema de coordenadas
        if brasil_shp.crs != src.crs:
            brasil_shp = brasil_shp.to_crs(src.crs)
        
        # Obter as geometrias do shapefile
        geometries = brasil_shp.geometry.values
        
        # Recortar o raster usando o shapefile
        out_image, out_transform = mask(dataset=src, shapes=geometries, crop=True)
        
        # Atualizar os metadados do raster recortado
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })
        
        # Salvar o raster recortado
        with rasterio.open(output_raster_path, "w", **out_meta) as dest:
            dest.write(out_image)
    
    print(f'Raster recortado salvo em: {output_raster_path}')
    return output_raster_path

# Função principal para capturar os argumentos da linha de comando
def main():
    if len(sys.argv) != 4:
        print("Uso correto: python recortar_raster.py raster.tif shapefile.shp output_raster.tif")
        sys.exit(1)

    raster_path = sys.argv[1]
    shapefile_path = sys.argv[2]
    output_raster_path = sys.argv[3]

    try:
        recortar_raster_com_shapefile(raster_path, shapefile_path, output_raster_path)
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

