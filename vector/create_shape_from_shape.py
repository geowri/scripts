import geopandas as gpd
import argparse
import sys

def exportar_linhas_e_atributos(shapefile_path, output_shapefile, atributo=None, valores=None, colunas=None):
    try:
        # Carregar o shapefile original
        gdf = gpd.read_file(shapefile_path)

        # Verificar o CRS (Sistema de Referência de Coordenadas)
        crs_original = gdf.crs
        print(f"Sistema de Referência de Coordenadas (CRS) original: {crs_original}")

        # Exibir a quantidade de linhas e colunas no shapefile original
        print(f"O shapefile original contém {len(gdf)} linhas e as seguintes colunas:")
        print(gdf.columns)

        # Se o atributo e valores forem especificados, filtrar com base neles
        if atributo and valores:
            # Converter os valores para uma lista (separar valores por espaços)
            valores = valores.split()

            # Filtrar as linhas com base no atributo e múltiplos valores especificados
            gdf_selecionado = gdf[gdf[atributo].isin(valores)].copy()

            # Verificar se algum registro foi encontrado
            if gdf_selecionado.empty:
                print(f"Nenhuma linha encontrada com {atributo} nos valores {valores}.")
                return
        else:
            # Se nenhum filtro de atributo e valor for especificado, selecionar todas as linhas
            gdf_selecionado = gdf.copy()

        # Se colunas forem especificadas, verificar se elas existem no shapefile
        if colunas:
            colunas_existentes = [coluna for coluna in colunas if coluna in gdf_selecionado.columns]
            colunas_faltantes = [coluna for coluna in colunas if coluna not in gdf_selecionado.columns]

            if colunas_faltantes:
                print(f"Essas colunas não foram encontradas no shapefile: {colunas_faltantes}")

            # Filtrar apenas as colunas existentes
            gdf_selecionado = gdf_selecionado[colunas_existentes + ['geometry']]  # Sempre manter a geometria
        else:
            # Se nenhuma coluna for especificada, exportar todas as colunas
            gdf_selecionado = gdf_selecionado.copy()

        # Manter o CRS ao exportar o novo shapefile
        gdf_selecionado.set_crs(crs=crs_original, inplace=True)

        # Exportar as linhas e colunas selecionadas para um novo shapefile
        gdf_selecionado.to_file(output_shapefile)
        print(f"Novo shapefile criado com as linhas e colunas selecionadas: {output_shapefile}")

    except Exception as e:
        print(f"Erro ao processar o shapefile: {e}")
        sys.exit(1)

def main():
    # Configuração dos argumentos da linha de comando
    parser = argparse.ArgumentParser(
        description="Exporta linhas e atributos específicos de um shapefile com base em um atributo e múltiplos valores (opcional) para um novo shapefile.\n",
        usage="%(prog)s shapefile_path output_shapefile [--atributo ATRIBUTO] [--valores VALORES] [--colunas COLUNAS [COLUNAS ...]]"
    )
    parser.add_argument('shapefile_path', type=str, help="Caminho do shapefile original")
    parser.add_argument('output_shapefile', type=str, help="Caminho do novo shapefile resultante")
    parser.add_argument('--atributo', type=str, help="Atributo a ser usado para selecionar as linhas (opcional)")
    parser.add_argument('--valores', type=str, help="Lista de valores do atributo para filtrar as linhas, separados por espaços (opcional)")
    parser.add_argument('--colunas', nargs='+', help="Lista de colunas a serem exportadas (opcional)")

    # Parse dos argumentos
    args = parser.parse_args()

    # Chamar a função para exportar as linhas e colunas
    exportar_linhas_e_atributos(
        args.shapefile_path, 
        args.output_shapefile, 
        args.atributo, 
        args.valores, 
        args.colunas or []
    )

if __name__ == "__main__":
    main()

