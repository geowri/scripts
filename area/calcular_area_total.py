#!/usr/bin/env python3

import os
import sys
import numpy as np
import rasterio
import pandas as pd

def verificar_entrada_existente(caminho):
    """
    Verifica se o arquivo ou diretório existe.
    """
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo ou diretório não encontrado: {caminho}")

def calcular_area_manchas(raster_path):
    """
    Calcula a área das manchas no raster.
    
    Parâmetros:
    - raster_path: Caminho para o raster.
    
    Retorna um dicionário com a área das manchas em metros quadrados e hectares.
    """
    with rasterio.open(raster_path) as src:
        raster_data = src.read(1)  # Ler a primeira banda
        
        # Extrair a resolução diretamente do raster
        pixel_area = src.res[0] * src.res[1]  # Área de cada pixel em metros quadrados

        # Obter os valores únicos e contagem de pixels
        valores_unicos, contagem = np.unique(raster_data, return_counts=True)

        # Calcular a área para cada valor único (mancha)
        areas_m2 = contagem * pixel_area  # Multiplica o número de pixels pela área de cada pixel em metros quadrados
        areas_ha = areas_m2 / 10000  # Converter de metros quadrados para hectares

        return dict(zip(valores_unicos, zip(areas_m2, areas_ha)))  # Retorna tanto a área em m² quanto em hectares

def salvar_areas_em_csv(areas_manchas, output_csv):
    """
    Salva as áreas das manchas em um arquivo CSV.
    
    Parâmetros:
    - areas_manchas: Dicionário com as áreas das manchas.
    - output_csv: Caminho do arquivo CSV de saída.
    """
    df = pd.DataFrame(columns=["Mancha", "Area_m2", "Area_ha"])
    
    # Use pd.concat corretamente
    df = pd.concat([pd.DataFrame({"Mancha": [mancha], "Area_m2": [area_m2], "Area_ha": [area_ha]})
                    for mancha, (area_m2, area_ha) in areas_manchas.items()],
                   ignore_index=True)
    
    df.to_csv(output_csv, index=False)
    print(f"Arquivo CSV salvo em: {output_csv}")

def main():
    if len(sys.argv) != 3:
        print("Uso correto: python calcular_areas_manchas.py <raster.tif> <output.csv>")
        sys.exit(1)

    # Capturar os argumentos da linha de comando
    raster_path = sys.argv[1]
    output_csv = sys.argv[2]

    # Verificar se o raster existe
    verificar_entrada_existente(raster_path)

    # Calcular as áreas das manchas para o raster
    areas_manchas = calcular_area_manchas(raster_path)

    # Salvar as áreas em um arquivo CSV
    salvar_areas_em_csv(areas_manchas, output_csv)

if __name__ == "__main__":
    main()
