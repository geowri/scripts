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

def calcular_area_manchas(raster_path, pixel_area):
    """
    Calcula a área das manchas no raster cortado.
    
    Parâmetros:
    - raster_path: Caminho para o raster cortado.
    - pixel_area: Área de cada pixel (resolução).
    
    Retorna um dicionário com a área das manchas.
    """
    with rasterio.open(raster_path) as src:
        raster_data = src.read(1)  # Ler a primeira banda
        valores_unicos, contagem = np.unique(raster_data, return_counts=True)

        # Calcular a área para cada valor único (mancha)
        areas_m2 = contagem * pixel_area  # Multiplica o número de pixels pela área de cada pixel em metros quadrados
        areas_ha = areas_m2 / 10000  # Converter de metros quadrados para hectares

        return dict(zip(valores_unicos, zip(areas_m2, areas_ha)))  # Retorna tanto a área em m² quanto em hectares

def salvar_areas_em_csv(areas_por_estado, output_csv):
    """
    Salva as áreas das manchas em um arquivo CSV.
    
    Parâmetros:
    - areas_por_estado: Dicionário com as áreas das manchas por estado.
    - output_csv: Caminho do arquivo CSV de saída.
    """
    df = pd.DataFrame(areas_por_estado)
    df.to_csv(output_csv, index=False)
    print(f"Arquivo CSV salvo em: {output_csv}")

def main():
    if len(sys.argv) != 4:
        print("Uso correto: python calcular_areas_manchas.py <diretorio_rasters> <resolucao_metros> <output.csv>")
        sys.exit(1)

    # Capturar os argumentos da linha de comando
    diretorio_rasters = sys.argv[1]
    resolucao = float(sys.argv[2])
    output_csv = sys.argv[3]

    # Calcular a área de cada pixel
    pixel_area = resolucao * resolucao

    # Listar os rasters no diretório
    rasters = [os.path.join(diretorio_rasters, f) for f in os.listdir(diretorio_rasters) if f.endswith('.tif')]

    areas_por_estado = {"Estado": [], "Mancha": [], "Area_m2": [], "Area_ha": []}

    # Calcular as áreas das manchas para cada raster
    for raster_path in rasters:
        estado_nome = os.path.basename(raster_path).replace("raster_", "").replace(".tif", "")
        areas_manchas = calcular_area_manchas(raster_path, pixel_area)

        for mancha, (area_m2, area_ha) in areas_manchas.items():
            areas_por_estado["Estado"].append(estado_nome)
            areas_por_estado["Mancha"].append(mancha)
            areas_por_estado["Area_m2"].append(area_m2)
            areas_por_estado["Area_ha"].append(area_ha)

    # Salvar as áreas em um arquivo CSV
    salvar_areas_em_csv(areas_por_estado, output_csv)

if __name__ == "__main__":
    main()