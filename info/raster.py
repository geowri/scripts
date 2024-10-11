#!/usr/bin/env python3
import sys
from osgeo import gdal

# Habilitar exceções no GDAL para tratar erros adequadamente
gdal.UseExceptions()

def verificar_projecao_raster(raster_path):
    """
    Verifica a projeção e exibe um resumo das informações de um arquivo raster.

    Parâmetros:
    raster_path (str): Caminho para o arquivo raster (.tif, .img, etc.).

    Retorno:
    None. Exibe o resultado e um resumo formatado e explicativo.
    """
    # Abrir o arquivo raster
    dataset = gdal.Open(raster_path)

    if dataset is None:
        raise ValueError(f"Não foi possível abrir o arquivo raster: {raster_path}")

    # Exibir as informações gerais sobre o raster
    print(f"INFO: Abertura do arquivo `{raster_path}` foi bem-sucedida.\n")

    # Dimensões do raster
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    print(f"Dimensões: {cols} colunas x {rows} linhas")

    # Número de bandas
    num_bands = dataset.RasterCount
    print(f"Número de Bandas: {num_bands}")

    # Tamanho de pixel
    geotransform = dataset.GetGeoTransform()
    if geotransform:
        pixel_size_x = geotransform[1]
        pixel_size_y = geotransform[5]
        print(f"Tamanho de Pixel: {pixel_size_x} x {abs(pixel_size_y)}")

        # Extensão (Bounding Box)
        origin_x = geotransform[0]
        origin_y = geotransform[3]
        extent_x = origin_x + (cols * pixel_size_x)
        extent_y = origin_y + (rows * pixel_size_y)
        print(f"Extensão (Bounding Box): ({origin_x:.6f}, {origin_y:.6f}) - ({extent_x:.6f}, {extent_y:.6f})")
    else:
        print("Não foi possível obter o geotransform.")

    # Projeção (WKT)
    projection = dataset.GetProjectionRef()
    if projection:
        print(f"Projeção (WKT):\n{projection}")
    else:
        print("O arquivo raster não possui uma projeção definida.")

    # Estatísticas das bandas
    for i in range(1, num_bands + 1):
        band = dataset.GetRasterBand(i)
        min_val, max_val, mean, stddev = band.GetStatistics(True, True)
        print(f"\nResumo da Banda {i}:")
        print(f"  Valor Mínimo: {min_val}")
        print(f"  Valor Máximo: {max_val}")
        print(f"  Média: {mean}")
        print(f"  Desvio Padrão: {stddev}")
        print(f"  Tipo de Dado: {gdal.GetDataTypeName(band.DataType)}")

    # Fechar o dataset
    dataset = None

    # Resumo explicativo
    print("\nResumo Explicativo:")
    print(f"O raster `{raster_path}` possui as seguintes características:")
    print(f"- Ele é composto por {cols} colunas e {rows} linhas, resultando em uma imagem raster de {cols * rows} pixels.")
    print(f"- O raster tem {num_bands} banda(s), que representam diferentes tipos de dados, como cor, intensidade ou outras variáveis.")
    if geotransform:
        print(f"- O tamanho de cada pixel é de {pixel_size_x:.2f} unidades na direção horizontal e {abs(pixel_size_y):.2f} unidades na direção vertical.")
        print(f"- A extensão geográfica do raster vai de ({origin_x:.6f}, {origin_y:.6f}) até ({extent_x:.6f}, {extent_y:.6f}), que representa a área coberta pela imagem.")
    else:
        print("- Não foi possível determinar a extensão geográfica ou o tamanho de pixel, o que pode indicar que o raster não possui informações geoespaciais bem definidas.")
    if projection:
        print(f"- O sistema de projeção usado é o seguinte: {projection[:50]}... (WKT completo disponível na saída acima).")
    else:
        print("- O raster não possui um sistema de projeção definido, o que significa que ele pode não estar associado a um sistema de coordenadas geográficas.")

# Função principal para capturar o argumento da linha de comando
def main():
    if len(sys.argv) != 2:
        print("Uso correto: python verificar_projecao_raster.py nome_do_raster.tif")
        sys.exit(1)

    raster_path = sys.argv[1]
    try:
        verificar_projecao_raster(raster_path)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()

