import geopandas as gpd
import argparse
import sys

def exportar_shapefile_para_csv(shapefile_path, output_csv, colunas):
    try:
        # Carregar o shapefile
        gdf = gpd.read_file(shapefile_path)
        
        # Exibir todas as colunas presentes no shapefile
        print("Colunas disponíveis no shapefile:")
        print(gdf.columns)

        # Verificar se as colunas especificadas existem no shapefile
        colunas_existentes = [coluna for coluna in colunas if coluna in gdf.columns]
        colunas_faltantes = [coluna for coluna in colunas if coluna not in gdf.columns]

        if colunas_faltantes:
            print(f"Essas colunas não foram encontradas no shapefile: {colunas_faltantes}")
        
        # Se não for especificada nenhuma coluna, exportar todas (exceto geometry)
        if not colunas_existentes:
            print("Nenhuma coluna válida foi especificada, exportando todas as colunas (exceto 'geometry').")
            gdf.drop(columns='geometry').to_csv(output_csv, index=False)
        else:
            print(f"Exportando as colunas: {colunas_existentes}")
            gdf[colunas_existentes].to_csv(output_csv, index=False)
        
        print(f"Shapefile exportado com sucesso para o arquivo CSV: {output_csv}")

    except Exception as e:
        print(f"Erro ao processar o shapefile: {e}")
        sys.exit(1)

def main():
    # Configuração dos argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Exporta atributos específicos de um shapefile para um CSV")
    parser.add_argument('shapefile_path', type=str, help="Caminho do shapefile a ser processado")
    parser.add_argument('output_csv', type=str, help="Caminho do arquivo CSV para salvar os resultados")
    parser.add_argument('--colunas', nargs='+', help="Lista de colunas a serem exportadas (opcional)")

    # Parse dos argumentos
    args = parser.parse_args()

    # Chamar a função de exportação
    exportar_shapefile_para_csv(args.shapefile_path, args.output_csv, args.colunas or [])

if __name__ == "__main__":
    main()

