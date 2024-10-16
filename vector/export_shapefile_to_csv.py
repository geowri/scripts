import geopandas as gpd
import argparse
import sys

def exportar_shapefile_para_csv(shapefile_path, output_csv, colunas, linhas, incluir_geometry):
    try:
        # Carregar o shapefile
        gdf = gpd.read_file(shapefile_path)

        # Exibir todas as colunas presentes no shapefile
        print("Colunas disponíveis no shapefile:")
        print(gdf.columns)

        # Se linhas forem especificadas, selecionar apenas essas linhas
        if linhas:
            max_index = len(gdf) - 1
            if any([linha > max_index or linha < 0 for linha in linhas]):
                print(f"Erro: Os índices de linhas devem estar entre 0 e {max_index}.")
                return
            gdf = gdf.iloc[linhas]

        # Verificar se as colunas especificadas existem no shapefile
        if colunas:
            colunas_existentes = [coluna for coluna in colunas if coluna in gdf.columns]
            colunas_faltantes = [coluna for coluna in colunas if coluna not in gdf.columns]

            if colunas_faltantes:
                print(f"Essas colunas não foram encontradas no shapefile: {colunas_faltantes}")
                return
        else:
            # Se não forem especificadas colunas, selecionar todas (exceto geometry se não solicitado)
            colunas_existentes = list(gdf.columns)
            if not incluir_geometry:
                colunas_existentes.remove('geometry')

        # Exportar as colunas selecionadas (com ou sem a geometria) para CSV
        if incluir_geometry and 'geometry' not in colunas_existentes:
            colunas_existentes.append('geometry')

        print(f"Exportando as colunas: {colunas_existentes}")
        gdf[colunas_existentes].to_csv(output_csv, index=False)

        print(f"Shapefile exportado com sucesso para o arquivo CSV: {output_csv}")

    except Exception as e:
        print(f"Erro ao processar o shapefile: {e}")
        sys.exit(1)

def main():
    # Configuração dos argumentos da linha de comando
    parser = argparse.ArgumentParser(
        description="Exporta atributos de um shapefile para um arquivo CSV, com a opção de especificar linhas e incluir/excluir a coluna geometry.\n",
        usage="%(prog)s shapefile_path output_csv [--colunas COLUNA [COLUNA ...]] [--linhas LINHAS [LINHAS ...]] [--incluir_geometry]"
    )
    parser.add_argument('shapefile_path', type=str, help="Caminho do shapefile a ser processado")
    parser.add_argument('output_csv', type=str, help="Caminho do arquivo CSV para salvar os resultados")
    parser.add_argument('--colunas', nargs='+', help="Lista de colunas a serem exportadas. Se não fornecida, exporta todas exceto 'geometry'.")
    parser.add_argument('--linhas', nargs='+', type=int, help="Índices das linhas a serem exportadas (opcional)")
    parser.add_argument('--incluir_geometry', action='store_true', help="Incluir a coluna geometry no CSV exportado.")

    # Parse dos argumentos
    args = parser.parse_args()

    # Chamar a função de exportação
    exportar_shapefile_para_csv(args.shapefile_path, args.output_csv, args.colunas, args.linhas, args.incluir_geometry)

if __name__ == "__main__":
    main()

