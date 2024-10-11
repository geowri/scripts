#!/usr/bin/env python3

import argparse
import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np

def recortar_raster_com_shapefile(raster_path, shapefile_path, output_raster_path):
    # Carregar o shapefile do Brasil
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

def calcular_areas_manchas(raster_path, min_valor, max_valor):
    # Abrir o raster recortado
    with rasterio.open(raster_path) as src:
        # Ler os dados do raster
        raster_data = src.read(1)
        
        # Obter a resolução espacial do raster (tamanho da célula)
        pixel_area = src.res[0] * src.res[1]
        
        # Dicionário para armazenar as áreas por valor
        areas_por_valor = {}
        
        # Calcular a área para cada valor dentro do intervalo
        for valor in range(min_valor, max_valor + 1):
            # Criar uma máscara para o valor atual
            mancha_mask = raster_data == valor
            
            # Calcular a área em unidades do sistema de coordenadas do raster
            area_total = np.sum(mancha_mask) * pixel_area
            
            # Armazenar o resultado
            areas_por_valor[valor] = area_total
            
            # Mostrar a área calculada para cada valor
            print(f'Área total para a mancha com valor {valor}: {area_total:.2f} unidades²')
        
        return areas_por_valor

if __name__ == "__main__":
    # Configurar o parser de argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Recortar um raster usando um shapefile e calcular a área de manchas.')
    parser.add_argument('raster_path', type=str, help='Caminho para o arquivo raster (mosaico).')
    parser.add_argument('shapefile_path', type=str, help='Caminho para o shapefile do Brasil.')
    parser.add_argument('output_raster_path', type=str, help='Caminho para salvar o raster recortado.')
    parser.add_argument('min_valor', type=int, help='Valor mínimo das manchas.')
    parser.add_argument('max_valor', type=int, help='Valor máximo das manchas.')

    # Ler os argumentos da linha de comando
    args = parser.parse_args()

    # Passo 1: Recortar o raster com o shapefile do Brasil
    raster_recortado = recortar_raster_com_shapefile(args.raster_path, args.shapefile_path, args.output_raster_path)

    # Passo 2: Calcular as áreas das manchas no raster recortado
    calcular_areas_manchas(raster_recortado, args.min_valor, args.max_valor)
