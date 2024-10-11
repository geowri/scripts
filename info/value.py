#!/usr/bin/env python3

import argparse
import rasterio
import numpy as np

def verificar_valores_raster(raster_path):
    # Abrir o mosaico raster
    with rasterio.open(raster_path) as src:
        # Ler os dados do raster
        raster_data = src.read(1)  # Lê a primeira banda
        
        # Calcular o valor mínimo e máximo
        valor_min = np.min(raster_data)
        valor_max = np.max(raster_data)
        
        print(f'Valor mínimo no raster: {valor_min}')
        print(f'Valor máximo no raster: {valor_max}')
    
    return valor_min, valor_max

if __name__ == "__main__":
    # Configurar o parser de argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Verificar o valor mínimo e máximo de um raster.")
    parser.add_argument('raster_path', type=str, help="Caminho para o arquivo raster (mosaico).")

    # Parse dos argumentos
    args = parser.parse_args()

    # Executar a função passando o caminho do raster como argumento
    verificar_valores_raster(args.raster_path)

