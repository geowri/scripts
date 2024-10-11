#!/usr/bin/env python3
import sys
from osgeo import gdal

# Habilitar exceções no GDAL para tratar erros adequadamente
gdal.UseExceptions()

def band_check(input_path):
    """
    Opens a raster image file and prints details about each band.

    Parameters:
        output_path (str): Path to the raster image file.
    """
    # Open the image file
    dataset = gdal.Open(input_path)

    if dataset is None:
        raise FileNotFoundError(f"Failed to open file: {output_path}")

    num_bands = dataset.RasterCount
    print(f"Number of bands: {num_bands}")

    # Print details of each band
    band_names = []
    for i in range(1, num_bands + 1):
        band = dataset.GetRasterBand(i)
        description = band.GetDescription() if band.GetDescription() else f"Band {i}"
        band_names.append(description)
        print(f"Band {i} - Description: {description}, Size: {band.XSize} x {band.YSize}")

# Example usage:
# output_path = 'path_to_your_image_file.tif'
# print_raster_band_details(output_path)



# Função principal para capturar o argumento da linha de comando
def main():
    if len(sys.argv) != 2:
        print("Uso correto: python resumo_raster.py nome_do_raster.tif")
        sys.exit(1)

    raster_path = sys.argv[1]
    try:
        band_check(raster_path)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()



