#!/usr/bin/env python3

from osgeo import gdal
import glob
import subprocess
import os
import sys
res = 0.1
# Habilita exceções no GDAL
#gdal.UseExceptions()

# Função para verificar se o diretório existe
def verificar_diretorio(raster_folder):
    """
    Verifica se o diretório especificado existe.
    
    Parâmetros:
    raster_folder (str): Caminho para o diretório de rasters que será verificado.
                         Caso o diretório não exista, será gerado um erro.
    
    Retorno:
    None. A função apenas gera uma exceção se o diretório não existir.
    """
    if not os.path.exists(raster_folder):
        raise ValueError(f"O diretório especificado não existe: {raster_folder}")

# Função para listar arquivos .tif no diretório
def listar_arquivos_tif(raster_folder):
    """
    Lista todos os arquivos .tif no diretório especificado.
    
    Parâmetros:
    raster_folder (str): Caminho para o diretório onde os arquivos raster (.tif) estão localizados.
    
    Retorno:
    demList (list): Lista de caminhos completos dos arquivos .tif encontrados no diretório.
                    Se não houver arquivos .tif, será gerada uma exceção.
    """
    demList = glob.glob(os.path.join(raster_folder, "*.tif"))
    if len(demList) == 0:
        raise ValueError(f"Nenhum arquivo raster encontrado no diretório especificado: {raster_folder}")
    else:
        print(f"Arquivos raster encontrados: {len(demList)}")
        print(f"Lista de arquivos: {demList}")
    return demList

# Função para executar o comando gdal_merge com paralelismo e compressão
def executar_gdal_merge(result_folder, demList):
    """
    Executa o gdal_merge para mosaicar rasters, com paralelismo e compressão.
    
    Parâmetros:
    result_folder (str): Caminho para o diretório onde o arquivo de mosaico será salvo.
    demList (list): Lista de arquivos raster (.tif) que serão combinados para formar o mosaico.
    
    Opções no comando:
    -ps 0.01 0.01: Define a resolução do mosaico em graus (neste caso, 0.01 graus).
    --config GDAL_NUM_THREADS ALL_CPUS: Utiliza todos os núcleos disponíveis do CPU para otimizar o processo.
    -o: Nome do arquivo de mosaico de saída.
    -co COMPRESS=DEFLATE: Aplica compressão DEFLATE ao arquivo de saída para reduzir o tamanho.
    -n 0: Define o valor de "no data" como 0.
    
    Retorno:
    None. Gera um erro se o gdal_merge falhar, ou imprime uma mensagem de sucesso.
    """
    # Desativar a verificação de espaço livre (opcional, se necessário)
    os.environ['CHECK_DISK_FREE_SPACE'] = 'FALSE'
    
    # Comando gdal_merge com paralelismo e compressão DEFLATE
    cmd = [
        "gdal_merge.py", "-ps", str(res), str(res), "--config", "GDAL_NUM_THREADS", "ALL_CPUS",
        "-o", os.path.join(result_folder, "mosaic.tif"), "-co", "COMPRESS=DEFLATE", "-n", "0"
    ] + demList
    
    # Executar o comando
    result = subprocess.call(cmd)
    
    if result != 0:
        raise RuntimeError("Erro ao executar gdal_merge.py")
    else:
        print("Mosaico criado com sucesso!")

# Função para criar VRT e exportar para outro TIF
def criar_vrt_exportar_tif(result_folder, demList):
    """
    Cria um arquivo VRT e exporta o resultado final para um TIF com compressão.
    
    Parâmetros:
    result_folder (str): Caminho para o diretório onde o VRT e o arquivo TIF final serão salvos.
    demList (list): Lista de arquivos raster (.tif) que serão utilizados para criar o VRT.
    
    Retorno:
    None. O VRT é criado e exportado como um arquivo TIF comprimido.
    """
    # Cria o VRT a partir dos rasters
    vrt = gdal.BuildVRT(os.path.join(result_folder, "mosaic.vrt"), demList)
    
    # Exporta o VRT para um arquivo TIF com compressão DEFLATE
    gdal.Translate(
        os.path.join(result_folder, "mosaic2.tif"), vrt, 
        xRes=res, yRes=res, creationOptions=["COMPRESS=DEFLATE"]
    )
    
    # Libera o objeto VRT da memória
    vrt = None
    print("VRT criado e exportado para TIF com sucesso!")

# Função para criar diretório, se não existir
def criar_diretorio(caminho_diretorio):
    """
    Cria o diretório de saída, caso não exista.
    
    Parâmetros:
    caminho_diretorio (str): Caminho completo para o diretório que será criado.
                             Caso o diretório já exista, a função apenas imprime uma mensagem de sucesso.
    
    Retorno:
    None. Cria o diretório ou gera uma mensagem de erro se ocorrer um problema.
    """
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

    # Executar o comando gdal_merge para criar o mosaico com paralelismo e compressão
    executar_gdal_merge(result_folder, demList)

    # Criar o VRT e exportar para um TIF final
    criar_vrt_exportar_tif(result_folder, demList)

if __name__ == "__main__":
    main()



