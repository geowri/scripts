#!/usr/bin/env python3
import sys
from osgeo import gdal

# Habilitar exceções no GDAL para tratar erros adequadamente
gdal.UseExceptions()

def metadata_raster(raster_path):
    """
    Verifica e exibe os metadados de um arquivo raster, incluindo projeção, dimensões,
    número de bandas, tamanho de pixel, extensão e estatísticas das bandas.
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
    # Print details of each band
    band_names = []
    for i in range(1, num_bands + 1):
        band = dataset.GetRasterBand(i)
        description = band.GetDescription() if band.GetDescription() else f"Band {i}"
        band_names.append(description)
        print(f"Band {i} - Description: {description}, Size: {band.XSize} x {band.YSize}")

    # Obter a geotransformação do raster
    geotransform = dataset.GetGeoTransform()

    # Verificar se a geotransformação está presente
    if geotransform is not None:
        pixel_size_x = geotransform[1]  # Tamanho do pixel na direção X
        pixel_size_y = geotransform[5]  # Tamanho do pixel na direção Y
        print(f"Tamanho de Pixel (resolução): {pixel_size_x} x {abs(pixel_size_y)}")

        # Extensão (Bounding Box)
        origin_x = geotransform[0]
        origin_y = geotransform[3]
        extent_x = origin_x + (cols * pixel_size_x)
        extent_y = origin_y + (rows * pixel_size_y)
        print(f"Extensão (Bounding Box): ({origin_x:.6f}, {origin_y:.6f}) - ({extent_x:.6f}, {extent_y:.6f})")
    else:
        print("Não foi possível obter a geotransformação do raster.")

    # Projeção (WKT)
    projection = dataset.GetProjectionRef()
    if projection is not None:
        print(f"Projeção (WKT):\n{projection}")
    else:
        print("O arquivo raster não possui uma projeção definida.")

    # Estatísticas das bandas
    for i in range(1, num_bands + 1):
        band = dataset.GetRasterBand(i)
        min_val, max_val, mean, stddev = band.GetStatistics(True, True)
        nodata_value = band.GetNoDataValue()

        print(f"\nResumo da Banda {i}:")
        print(f"  Valor Mínimo: {min_val:.4f}")
        print(f"  Valor Máximo: {max_val:.4f}")
        print(f"  Média: {mean:.4f}")
        print(f"  Desvio Padrão: {stddev:.4f}")
        print(f"  Tipo de Dado: {gdal.GetDataTypeName(band.DataType)}")

        # Exibir valor de NoData se existir
        if nodata_value is not None:
            print(f"  Valor NoData: {nodata_value}")
        else:
            print("  Valor NoData: Não Definido")

    # Fechar o dataset
    dataset = None

# Função principal para capturar o argumento da linha de comando
def main():
    if len(sys.argv) != 2:
        print("Uso correto: python verificar_metadados_raster.py nome_do_raster.tif")
        sys.exit(1)

    raster_path = sys.argv[1]
    try:
        metadata_raster(raster_path)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
