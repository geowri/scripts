#!/usr/bin/env python3
from osgeo import gdal
import sys

def verificar_resolucao_raster(raster_path):
    """
    Verifica e exibe a resolução de um arquivo raster.

    Parâmetros:
    raster_path (str): Caminho para o arquivo raster (.tif, .img, etc.).

    Retorno:
    None. Imprime a resolução do raster.
    """
    # Abrir o arquivo raster
    dataset = gdal.Open(raster_path)
    if dataset is None:
        raise ValueError(f"Não foi possível abrir o raster: {raster_path}")

    # Obter a geotransformação do raster
    geotransform = dataset.GetGeoTransform()
    if geotransform is not None:
        pixel_size_x = geotransform[1]  # Tamanho do pixel na direção X
        pixel_size_y = geotransform[5]  # Tamanho do pixel na direção Y (normalmente negativo)
        
        # Exibir a resolução do raster
        print(f"Resolução do raster (tamanho dos pixels):")
        print(f"  Tamanho do pixel em X (largura): {pixel_size_x}")
        print(f"  Tamanho do pixel em Y (altura): {abs(pixel_size_y)}")
    else:
        print("Não foi possível obter a geotransformação do raster.")

    # Fechar o dataset
    dataset = None

# Função principal para capturar o argumento da linha de comando
def main():
    if len(sys.argv) != 2:
        print("Uso correto: python verificar_resolucao_raster.py raster_file.tif")
        sys.exit(1)

    raster_path = sys.argv[1]
    try:
        verificar_resolucao_raster(raster_path)
    except ValueError as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

