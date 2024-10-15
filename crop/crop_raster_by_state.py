#!/usr/bin/env python3

import os
import sys
import rasterio
import geopandas as gpd
from rasterio.mask import mask

def verificar_entrada_existente(caminho):
    """
    Verifica se o arquivo ou diretório existe.
    """
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo ou diretório não encontrado: {caminho}")

def cortar_raster_por_estado(raster_path, estados_shp_path, output_dir):
    """
    Corta o raster para cada estado do shapefile e salva no diretório de saída.
    
    Parâmetros:
    - raster_path: Caminho para o raster de entrada.
    - estados_shp_path: Caminho para o shapefile dos estados da Amazônia Legal.
    - output_dir: Diretório onde os rasters cortados serão salvos.
    
    Retorna uma lista com os caminhos dos rasters cortados.
    """
    verificar_entrada_existente(raster_path)
    verificar_entrada_existente(estados_shp_path)

    # Carregar o shapefile dos estados
    estados_shp = gpd.read_file(estados_shp_path)

    # Abrir o raster de entrada
    raster_cortado_paths = []
    with rasterio.open(raster_path) as src:
        for estado in estados_shp.itertuples():
            geometria_estado = [estado.geometry]

            # Cortar o raster para o estado
            out_image, out_transform = mask(src, geometria_estado, crop=True)
            
            # Atualizar metadados
            out_meta = src.meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform
            })

            # Caminho do arquivo cortado
            output_raster_path = os.path.join(output_dir, f"raster_{estado.nome}.tif")
            raster_cortado_paths.append(output_raster_path)

            # Salvar o raster cortado
            with rasterio.open(output_raster_path, "w", **out_meta) as dest:
                dest.write(out_image)

            print(f"Raster cortado para o estado {estado.nome} salvo em: {output_raster_path}")

    return raster_cortado_paths

def main():
    if len(sys.argv) != 4:
        print("Uso correto: python cortar_raster_por_estado.py <raster.tif> <estados.shp> <output_dir>")
        sys.exit(1)

    # Capturar os argumentos da linha de comando
    raster_path = sys.argv[1]
    estados_shp_path = sys.argv[2]
    output_dir = sys.argv[3]

    # Verificar se os caminhos de entrada existem
    verificar_entrada_existente(raster_path)
    verificar_entrada_existente(estados_shp_path)
    
    # Criar o diretório de saída, se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Cortar o raster para cada estado e salvar no diretório de saída
    cortar_raster_por_estado(raster_path, estados_shp_path, output_dir)

if __name__ == "__main__":
    main()

