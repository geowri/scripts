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

def calcular_area_manchas(raster_path, valor_min, valor_max):
    """
    Calcula a área das manchas no raster dentro de um intervalo de valores.
    
    Parâmetros:
    - raster_path: Caminho para o raster.
    - valor_min: Valor mínimo do intervalo de manchas a serem processadas.
    - valor_max: Valor máximo do intervalo de manchas a serem processadas.
    
    Retorna um dicionário com a área das manchas em metros quadrados e hectares.
    """
    with rasterio.open(raster_path) as src:
        # Extrair a resolução diretamente do raster
        pixel_area = src.res[0] * src.res[1]  # Calcular a área do pixel (em metros quadrados)

        raster_data = src.read(1)  # Ler a primeira banda
        
        # Filtrar os valores únicos dentro do intervalo definido
        valores_unicos, contagem = np.unique(raster_data, return_counts=True)
        filtro = (valores_unicos >= valor_min) & (valores_unicos <= valor_max)
        valores_filtrados = valores_unicos[filtro]
        contagem_filtrada = contagem[filtro]

        # Calcular a área para cada valor filtrado (mancha)
        areas_m2 = contagem_filtrada * pixel_area  # Área em metros quadrados
        areas_ha = areas_m2 / 10000  # Converter de metros quadrados para hectares

        return dict(zip(valores_filtrados, zip(areas_m2, areas_ha)))  # Retorna as áreas em m² e ha

def salvar_areas_em_csv(areas_manchas, output_csv):
    """
    Salva as áreas das manchas em um arquivo CSV.
    
    Parâmetros:
    - areas_manchas: Dicionário com as áreas das manchas.
    - output_csv: Caminho do arquivo CSV de saída.
    """
    # Lista para armazenar os DataFrames
    lista_df = []

    # Criar DataFrames para cada mancha e concatenar no final
    for mancha, (area_m2, area_ha) in areas_manchas.items():
        df = pd.DataFrame({"Mancha": [mancha], "Area_m2": [area_m2], "Area_ha": [area_ha]})
        lista_df.append(df)
    
    # Concatenar todos os DataFrames
    df_final = pd.concat(lista_df, ignore_index=True)

    # Salvar o DataFrame concatenado em CSV
    df_final.to_csv(output_csv, index=False)
    print(f"Arquivo CSV salvo em: {output_csv}")

def main():
    if len(sys.argv) != 5:
        print("Uso correto: python calcular_areas_manchas.py <raster.tif> <valor_min> <valor_max> <output.csv>")
        sys.exit(1)

    # Capturar os argumentos da linha de comando
    raster_path = sys.argv[1]
    valor_min = int(sys.argv[2])
    valor_max = int(sys.argv[3])
    output_csv = sys.argv[4]

    # Verificar se o raster existe
    verificar_entrada_existente(raster_path)

    # Calcular as áreas das manchas para o raster dentro do intervalo de valores
    areas_manchas = calcular_area_manchas(raster_path, valor_min, valor_max)

    # Salvar as áreas em um arquivo CSV
    salvar_areas_em_csv(areas_manchas, output_csv)

if __name__ == "__main__":
    main()

