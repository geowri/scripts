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
    return demList

# Função para mosaicar dois rasters de cada vez
def mosaicar_em_partes(result_folder, demList):
    temp_mosaics = []
    
    # Mosaicar dois rasters de cada vez
    for i in range(0, len(demList), 2):
        parte_rasters = demList[i:i + 2]
        
        # Nome do arquivo de mosaico parcial
        output_file = os.path.join(result_folder, f"mosaic_parcial_{i//2}.tif")
        temp_mosaics.append(output_file)
        
        # Comando gdalwarp com paralelismo, compressão DEFLATE e definição de resolução
        cmd = [
            "gdalwarp", "-multi", "-wo", "NUM_THREADS=ALL_CPUS", "-co", "COMPRESS=DEFLATE",
            "-r", "near", "-overwrite"
        ]
        
        # Adiciona o parâmetro de resolução (-tr) se a variável 'res' estiver definida
        if res:
            cmd += ["-tr", str(res), str(res)]
        
        cmd += parte_rasters + [output_file]

        # Executar o comando
        result = subprocess.call(cmd)
        if result != 0:
            raise RuntimeError(f"Erro ao executar gdalwarp para {parte_rasters}")
        else:
            print(f"Mosaico parcial {output_file} criado com sucesso!")

    return temp_mosaics

# Função para combinar os mosaicos parciais em um mosaico final
def combinar_mosaicos_finais(result_folder, temp_mosaics):
    # Nome do arquivo final
    output_file_final = os.path.join(result_folder, "mosaic_final.tif")

    # Comando gdalwarp para combinar os mosaicos parciais
    cmd = [
        "gdalwarp", "-multi", "-wo", "NUM_THREADS=ALL_CPUS", "-co", "COMPRESS=DEFLATE",
        "-r", "near", "-overwrite"
    ]
    
    # Adiciona o parâmetro de resolução (-tr) se a variável 'res' estiver definida
    if res:
        cmd += ["-tr", str(res), str(res)]

    cmd += temp_mosaics + [output_file_final]

    # Executar o comando
    result = subprocess.call(cmd)
    if result != 0:
        raise RuntimeError("Erro ao combinar os mosaicos parciais")
    else:
        print("Mosaico final criado com sucesso!")

# Função principal para capturar os argumentos da linha de comando
def main():
    if len(sys.argv) != 3:
        print("Uso correto: python mosaico_rasters.py <raster_folder> <result_folder>")
        sys.exit(1)
    
    # Caminho da pasta onde os arquivos raster estão
    raster_folder = sys.argv[1]
    
    # Caminho do diretório onde os resultados serão salvos
    result_folder = sys.argv[2]

    # Verifica e cria o diretório de resultados, se não existir
    os.makedirs(result_folder, exist_ok=True)

    # Executar as funções
    verificar_diretorio(raster_folder)
    demList = listar_arquivos_tif(raster_folder)

    # Mosaicar em partes e obter lista de mosaicos parciais
    temp_mosaics = mosaicar_em_partes(result_folder, demList)

    # Combinar os mosaicos parciais em um único mosaico final
    combinar_mosaicos_finais(result_folder, temp_mosaics)

if __name__ == "__main__":
    main()
