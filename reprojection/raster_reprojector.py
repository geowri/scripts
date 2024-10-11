#!/usr/bin/env python3
import sys
import argparse
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

def main():
    # Criar um parser de argumentos da linha de comando
    parser = argparse.ArgumentParser(
        description="Script para reprojetar rasters para diferentes sistemas de coordenadas (EPSG ou Proj4)."
    )

    # Argumentos
    parser.add_argument("input_raster", type=str, nargs="?", help="Caminho para o arquivo raster de entrada (.tif, .img, etc.).")
    parser.add_argument("output_raster", type=str, nargs="?", help="Caminho para o arquivo raster de saída reprojetado.")
    parser.add_argument("target_srs", type=str, nargs="?", help="Projeção de destino (EPSG:xxxx ou Proj4).")
    parser.add_argument("--list", action="store_true", help="Lista algumas projeções comuns disponíveis para reprojeção.")

    # Analisar os argumentos
    args = parser.parse_args()

    # Exibir a lista de projeções se a opção --list for utilizada
    if args.list:
        listar_projecoes()
        sys.exit(0)

    # Verificar se os parâmetros obrigatórios foram fornecidos
    if not args.input_raster or not args.output_raster or not args.target_srs:
        parser.print_help()  # Exibir a ajuda se faltar argumentos
        sys.exit(1)

    # Tentar reprojetar o raster
    try:
        reprojetar_raster(args.input_raster, args.output_raster, args.target_srs)
    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
