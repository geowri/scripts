import geopandas as gpd
import argparse
import sys

def exportar_shapefile_para_csv(shapefile_path, output_csv):
    try:
        # Carregar o shapefile
        gdf = gpd.read_file(shapefile_path)
        
        # Exibir todas as colunas presentes no shapefile
        print("Colunas disponíveis no shapefile:")
        print(gdf.columns)

        # Exportar todas as colunas (exceto a coluna 'geometry') para um CSV
        gdf.drop(columns='geometry').to_csv(output_csv, index=False)
        print(f"Shapefile exportado com sucesso para o arquivo CSV: {output_csv}")

    except Exception as e:
        print(f"Erro ao processar o shapefile: {e}")
        sys.exit(1)

def main():
    # Configuração dos argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Exporta todos os atributos de um shapefile para um CSV")
    parser.add_argument('shapefile_path', type=str, help="Caminho do shapefile a ser processado")
    parser.add_argument('output_csv', type=str, help="Caminho do arquivo CSV para salvar os resultados")

    # Parse dos argumentos
    args = parser.parse_args()

    # Chamar a função de exportação
    exportar_shapefile_para_csv(args.shapefile_path, args.output_csv)

if __name__ == "__main__":
    main()

