import argparse
import rasterio
import numpy as np

def calcular_areas_manchas(raster_path, min_valor, max_valor):
    # Abrir o mosaico raster
    with rasterio.open(raster_path) as src:
        # Obter a resolução espacial do raster (tamanho da célula)
        pixel_area_m2 = src.res[0] * src.res[1]  # Largura x Altura da célula em metros quadrados
        pixel_area_ha = pixel_area_m2 / 10_000   # Converter de metros quadrados para hectares

        # Dicionário para armazenar as áreas por valor
        areas_por_valor = {valor: 0 for valor in range(min_valor, max_valor + 1)}

        # Processar o raster em blocos
        for ji, window in src.block_windows(1):  # Ler por blocos
            # Ler dados do bloco
            raster_data = src.read(1, window=window)

            # Calcular a área para cada valor dentro do intervalo
            for valor in range(min_valor, max_valor + 1):
                # Criar uma máscara para o valor atual
                mancha_mask = raster_data == valor

                # Calcular a área em metros quadrados e hectares para o bloco
                area_total_m2 = np.sum(mancha_mask) * pixel_area_m2
                area_total_ha = area_total_m2 / 10_000

                # Acumular as áreas para cada valor
                areas_por_valor[valor] += area_total_m2

        # Exibir os resultados
        for valor, area_total_m2 in areas_por_valor.items():
            area_total_ha = area_total_m2 / 10_000
            print(f'Área total para a mancha com valor {valor}: {area_total_m2:.2f} m² ({area_total_ha:.4f} ha)')

    return areas_por_valor

if __name__ == "__main__":
    # Configurar os argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Calcular áreas de manchas em um raster mosaico.')
    parser.add_argument('raster_path', type=str, help='Caminho para o arquivo raster (mosaico).')
    parser.add_argument('min_valor', type=int, help='Valor mínimo das manchas.')
    parser.add_argument('max_valor', type=int, help='Valor máximo das manchas.')

    # Ler os argumentos
    args = parser.parse_args()

    # Chamar a função com os argumentos da linha de comando
    calcular_areas_manchas(args.raster_path, args.min_valor, args.max_valor)

