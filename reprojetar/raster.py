#!/usr/bin/env python3
import sys
from osgeo import gdal

# Lista de algumas projeções comuns
PROJECTIONS = {
    'WGS 84 / Pseudo-Mercator': 'EPSG:3857',
    'WGS 84': 'EPSG:4326',
    'SIRGAS 2000 / Brazil Mercator': 'EPSG:5641',
    'South America Albers Equal Area Conic (ESRI)': 'ESRI:102033',
    'South America Albers Equal Area Conic (EPSG)': 'EPSG:5880',
    'UTM Zone 23S (WGS 84)': 'EPSG:32723',
    'UTM Zone 24S (WGS 84)': 'EPSG:32724',
    'South America Lambert Equal Area Conic': 'EPSG:3035',
    'Azimuthal Equidistant (World)': 'EPSG:54032',
}

def reprojetar_raster(input_raster, output_raster, target_srs):
    """
    Reprojeta um raster para uma nova projeção utilizando o método de vizinho mais próximo.
    
    Parâmetros:
    - input_raster (str): Caminho para o arquivo raster de entrada.
    - output_raster (str): Caminho para o arquivo raster de saída reprojetado.
    - target_srs (str): Sistema de referência de destino no formato EPSG ou Proj4 (ex: 'EPSG:4326' ou '+proj=longlat +datum=WGS84 +no_defs').
    """
    # Abrir o dataset do raster de entrada
    src_ds = gdal.Open(input_raster)
    if src_ds is None:
        raise ValueError(f"Não foi possível abrir o raster {input_raster}")

    # Definir a projeção de destino
    warp_options = gdal.WarpOptions(dstSRS=target_srs, resampleAlg='near')

    # Reprojetar o raster usando o método de vizinho mais próximo
    print(f"Reprojetando o raster para {target_srs} usando Vizinho Mais Próximo...")
    gdal.Warp(output_raster, src_ds, options=warp_options)

    print(f"Reprojeção concluída. Arquivo salvo em {output_raster}")

def listar_projecoes():
    """
    Lista algumas das projeções mais comuns para reprojeção com seus códigos EPSG e ESRI.
    """
    print("\nProjeções comuns disponíveis para reprojeção:\n")
    for proj, code in PROJECTIONS.items():
        print(f"{proj}: {code}")
    print("\nVocê também pode utilizar códigos EPSG ou strings Proj4 diretamente.")

# Função principal para capturar os argumentos da linha de comando
def main():
    if len(sys.argv) != 4:
        print("Uso correto: script.py input_raster.tif output_raster.tif EPSG:xxxx")
        print("Ou para Proj4: script.py input_raster.tif output_raster.tif '+proj=...'")
        listar_projecoes()  # Mostrar a lista de projeções possíveis
        sys.exit(1)

    input_raster = sys.argv[1]
    output_raster = sys.argv[2]
    target_srs = sys.argv[3]  # Projeção de destino fornecida pelo usuário

    try:
        reprojetar_raster(input_raster, output_raster, target_srs)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()

