#!/usr/bin/env python3

from osgeo import gdal
import glob
import os
import sys

#res = 0.0002694945852358564
res = 0.001

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
    return demList

# Função para criar o VRT
def criar_vrt(result_folder, demList):
    """
    Cria um arquivo VRT a partir dos rasters listados.
    
    Parâmetros:
    result_folder (str): Caminho para o diretório onde o arquivo VRT será salvo.
    demList (list): Lista de arquivos raster (.tif) que serão utilizados para criar o VRT.
    
    Retorno:
    None. O VRT é criado e salvo no diretório especificado.
    """
    vrt_path = os.path.join(result_folder, "mosaic.vrt")
    
    # Cria o VRT
    vrt = gdal.BuildVRT(vrt_path, demList, options=gdal.BuildVRTOptions(resolution='highest', srcNodata=0, VRTNodata=0))
    
    if vrt is None:
        raise RuntimeError("Erro ao criar o VRT.")
    else:
        print(f"VRT criado com sucesso em: {vrt_path}")
    
    return vrt_path

# Função para exportar o VRT para um TIF (opcional)
def exportar_vrt_para_tif(vrt_path, result_folder):
    """
    Exporta o VRT criado para um arquivo TIF com compressão DEFLATE.
    
    Parâmetros:
    vrt_path (str): Caminho para o arquivo VRT.
    result_folder (str): Caminho para o diretório onde o TIF final será salvo.
    
    Retorno:
    None. O TIF é criado e salvo no diretório especificado.
    """
    tif_output = os.path.join(result_folder, "mosaic_final.tif")
    
    # Exporta o VRT para um arquivo TIF
    gdal.Translate(
        tif_output, vrt_path, 
        xRes=res, yRes=res, creationOptions=["COMPRESS=DEFLATE"]
    )
    
    print(f"Mosaico exportado para TIF em: {tif_output}")

# Função principal para capturar os argumentos da linha de comando
def main():
    if len(sys.argv) != 3:
        print("Uso correto: python mosaico_rasters.py <raster_folder> <result_folder>")
        sys.exit(1)
    
    # Caminho da pasta onde os arquivos raster estão
    raster_folder = sys.argv[1]
    
    # Caminho do diretório onde os resultados serão salvos
    result_folder = sys.argv[2]

    # Verifica e cria diretório de saída, se não existir
    os.makedirs(result_folder, exist_ok=True)
    verificar_diretorio(raster_folder)
    
    # Lista os arquivos .tif na pasta
    demList = listar_arquivos_tif(raster_folder)

    # Cria o VRT a partir dos rasters listados
    vrt_path = criar_vrt(result_folder, demList)

    # Opcional: exportar o VRT para um TIF final
    exportar_vrt_para_tif(vrt_path, result_folder)

if __name__ == "__main__":
    main()

