import geopandas as gpd
import argparse
import sys

def exportar_duas_linhas(shapefile_path, output_shapefile, linhas):
    try:
        # Carregar o shapefile original
        gdf = gpd.read_file(shapefile_path)
        
        # Exibir a quantidade de linhas no shapefile original
        print(f"O shapefile original contém {len(gdf)} linhas.")

        # Verificar se os índices fornecidos são válidos
        max_index = len(gdf) - 1
        if any([linha > max_index or linha < 0 for linha in linhas]):
            print(f"Erro: Os índices devem estar entre 0 e {max_index}.")
            return

        # Selecionar as duas linhas com base nos índices fornecidos
        gdf_selecionado = gdf.iloc[linhas]

        # Exportar as duas linhas para um novo shapefile
        gdf_selecionado.to_file(output_shapefile)
        print(f"Novo shapefile criado com as duas linhas: {output_shapefile}")

    except Exception as e:
        print(f"Erro ao processar o shapefile: {e}")
        sys.exit(1)

def main():
    # Configuração dos argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Exporta duas linhas específicas de um shapefile para um novo shapefile")
    parser.add_argument('shapefile_path', type=str, help="Caminho do shapefile original")
    parser.add_argument('output_shapefile', type=str, help="Caminho do novo shapefile")
    parser.add_argument('linhas', nargs=2, type=int, help="Índices das duas linhas a serem exportadas (0-based)")

    # Parse dos argumentos
    args = parser.parse_args()

    # Chamar a função para exportar as duas linhas
    exportar_duas_linhas(args.shapefile_path, args.output_shapefile, args.linhas)

if __name__ == "__main__":
    main()

