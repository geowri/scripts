#!/usr/bin/env python3

import argparse
import geopandas as gpd

def metadata_vetor(vector_path):
    """
    Verifica os metadados e atributos de um arquivo vetorial (shapefile, GeoJSON, etc.).
    
    Parâmetros:
    vector_path (str): Caminho para o arquivo vetorial.
    
    Retorno:
    None. Exibe os metadados e valores estatísticos dos atributos numéricos.
    """
    # Carregar o arquivo vetorial
    gdf = gpd.read_file(vector_path)
    
    # Verificar se o arquivo foi carregado corretamente
    if gdf.empty:
        raise ValueError(f"Erro: O arquivo {vector_path} não contém dados ou não foi carregado corretamente.")
    
    # Exibir informações básicas
    print(f"\nArquivo vetorial carregado: {vector_path}")
    print(f"Número de geometrias (features): {len(gdf)}")
    print(f"Tipo de geometria: {gdf.geom_type.iloc[0]}")
    
    # Exibir o CRS (Sistema de Coordenadas de Referência)
    print(f"Sistema de Coordenadas (CRS): {gdf.crs}")
    
    # Extensão (Bounding Box)
    minx, miny, maxx, maxy = gdf.total_bounds
    print(f"Extensão geográfica (Bounding Box):")
    print(f"  Min X: {minx:.6f}, Min Y: {miny:.6f}")
    print(f"  Max X: {maxx:.6f}, Max Y: {maxy:.6f}")
    
    # Exibir as colunas
    print(f"\nAtributos presentes: {list(gdf.columns)}")
    
    # Obter a lista de colunas numéricas
    colunas_numericas = gdf.select_dtypes(include=['number']).columns.tolist()
    
    # Verificar se há colunas numéricas
    if not colunas_numericas:
        print("\nO arquivo vetorial não possui atributos numéricos.")
        return
    
    # Para cada coluna numérica, calcular o valor mínimo, máximo, média e desvio padrão
    print("\nEstatísticas dos atributos numéricos:")
    for coluna in colunas_numericas:
        valor_min = gdf[coluna].min()
        valor_max = gdf[coluna].max()
        media = gdf[coluna].mean()
        desvio_padrao = gdf[coluna].std()

        print(f"Atributo: {coluna}")
        print(f"  Valor mínimo: {valor_min}")
        print(f"  Valor máximo: {valor_max}")
        print(f"  Média: {media}")
        print(f"  Desvio Padrão: {desvio_padrao}\n")

def main():
    # Configurar o parser de argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Verificar metadados e valores dos atributos numéricos de um arquivo vetorial (shapefile, GeoJSON, etc.).")
    parser.add_argument('vector_path', type=str, help="Caminho para o arquivo vetorial (shapefile, GeoJSON, etc.).")

    # Parse dos argumentos
    args = parser.parse_args()

    # Executar a função passando o caminho do arquivo vetorial como argumento
    metadata_vetor(args.vector_path)

if __name__ == "__main__":
    main()
