#!/usr/bin/env python3

from osgeo import gdal
import glob
import subprocess
import os
import sys

res = None
#res = 0.0002694945852358564

# Função para verificar se o diretório existe
def verificar_diretorio(raster_folder):
    if not os.path.exists(raster_folder):
        raise ValueError(f"O diretório especificado não existe: {raster_folder}")

# Função para listar arquivos .tif no diretório
def listar_arquivos_tif(raster_folder):
    demList = glob.glob(os.path.join(raster_folder, "*.tif"))
    if len(demList) == 0:
        raise ValueError(f"Nenhum arquivo raster encontrado no diretório especificado: {raster_folder}")
    else:
        print(f"Arquivos raster encontrados: {len(demList)}")
        print(f"Lista de arquivos: {demList}")
    return demList

# Função para executar o comando gdalwarp com paralelismo, compressão e resolução
def executar_gdalwarp(result_folder, demList):
    """
    Executa o gdalwarp para mosaicar rasters, com paralelismo, compressão e resolução.
    
    Parâmetros:
    result_folder (str): Caminho para o diretório onde o arquivo de mosaico será salvo.
    demList (list): Lista de arquivos raster (.tif) que serão combinados para formar o mosaico.
    
    Opções no comando:
    -multi: Utiliza múltiplos núcleos do processador.
    -wo: Define o uso de múltiplos núcleos com ALL_CPUS.
    -tr: Define a resolução de saída (res).
    -co COMPRESS=DEFLATE: Aplica compressão DEFLATE ao arquivo de saída para reduzir o tamanho.
    
    Retorno:
    None. Gera um erro se o gdalwarp falhar, ou imprime uma mensagem de sucesso.
    """
    # Comando gdalwarp com paralelismo, compressão DEFLATE e resolução
    cmd = [
        "gdalwarp", "-multi", "-wo", "NUM_THREADS=ALL_CPUS", "-co", "COMPRESS=DEFLATE", "-r", "near", 
        "-overwrite"
    ]

    # Adiciona o parâmetro de resolução (-tr) se a variável 'res' estiver definida
    if res:
        cmd += ["-tr", str(res), str(res)]
    
    cmd += demList + [os.path.join(result_folder, "mosaic.tif")]
    
    # Executar o comando
    result = subprocess.call(cmd)
    
    if result != 0:
        raise RuntimeError("Erro ao executar gdalwarp")
    else:
        print("Mosaico criado com sucesso!")

# Função para criar VRT e exportar para outro TIF
def criar_vrt_exportar_tif(result_folder, demList):
    vrt = gdal.BuildVRT(os.path.join(result_folder, "mosaic.vrt"), demList)
    gdal.Translate(
        os.path.join(result_folder, "mosaic2.tif"), vrt, 
        creationOptions=["COMPRESS=DEFLATE"]
    )
    vrt = None
    print("VRT criado e exportado para TIF com sucesso!")

# Função para criar diretório, se não existir
def criar_diretorio(caminho_diretorio):
    try:
        os.makedirs(caminho_diretorio, exist_ok=True)
        print(f"Diretório '{caminho_diretorio}' criado com sucesso!")
    except OSError as e:
        print(f"Erro ao criar o diretório: {e}")

# Função principal para capturar os argumentos da linha de comando
def main():
    if len(sys.argv) != 3:
        print("Uso correto: python mosaico_rasters.py <raster_folder> <result_folder>")
        sys.exit(1)
    
    # Caminho da pasta onde os arquivos raster estão
    raster_folder = sys.argv[1]
    
    # Caminho do diretório onde os resultados serão salvos
    result_folder = sys.argv[2]

    # Executar as funções
    criar_diretorio(result_folder)  # Cria o diretório de resultados, se não existir
    verificar_diretorio(raster_folder)  # Verifica se a pasta de rasters existe
    demList = listar_arquivos_tif(raster_folder)  # Lista os arquivos .tif na pasta

    # Executar o comando gdalwarp para criar o mosaico com paralelismo e compressão
    executar_gdalwarp(result_folder, demList)

    # Criar o VRT e exportar para um TIF final
    criar_vrt_exportar_tif(result_folder, demList)

if __name__ == "__main__":
    main()
