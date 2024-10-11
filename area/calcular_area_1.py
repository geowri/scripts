import argparse
import rasterio
import numpy as np

def calcular_areas_manchas(raster_path, min_valor, max_valor):
    # Abrir o mosaico raster
    with rasterio.open(raster_path) as src:
        # Ler os dados do raster
        raster_data = src.read(1)  # Lê a primeira banda

        # Obter a resolução espacial do raster (tamanho da célula)
        pixel_area = src.res[0] * src.res[1]  # Largura x Altura da célula

        # Dicionário para armazenar as áreas por valor
        areas_por_valor = {}

        # Calcular a área para cada valor dentro do intervalo
        for valor in range(min_valor, max_valor + 1):
            # Criar uma máscara para o valor atual
            mancha_mask = raster_data == valor

            # Calcular a área em unidades do sistema de coordenadas do raster
            area_total = np.sum(mancha_mask) * pixel_area

            # Armazenar o resultado
            areas_por_valor[valor] = area_total

            # Mostrar a área calculada para cada valor
            print(f'Área total para a mancha com valor {valor}: {area_total:.2f} unidades²')

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

