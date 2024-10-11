#!/usr/bin/env python3

from osgeo import gdal
import glob
import subprocess
import os
import sys

res = 0.0002694945852358564

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

# Função para mosaicar um raster por vez
def mosaicar_em_partes(result_folder, demList):
    temp_mosaics = []
    temp_mosaic = None  # Variável para armazenar o mosaico temporário

    # Mosaicar um raster por vez
    for i, raster in enumerate(demList):
        # Se já houver um mosaico parcial, o próximo raster será combinado com ele
        if temp_mosaic is None:
            # O primeiro raster é apenas copiado
            temp_mosaic = raster
        else:
            # Nome do arquivo de mosaico parcial
            output_file = os.path.join(result_folder, f"mosaic_parcial_{i}.tif")
            temp_mosaics.append(output_file)

            # Comando gdal_merge com paralelismo e compressão DEFLATE
            cmd = [
                "gdal_merge.py", "-ps", str(res), str(res), "--config", "GDAL_NUM_THREADS", "ALL_CPUS",
                "-o", output_file, "-co", "COMPRESS=DEFLATE", "-n", "0",
                temp_mosaic, raster  # Combine o mosaico temporário com o próximo raster
            ]

            # Executar o comando
            result = subprocess.call(cmd)
            if result != 0:
                raise RuntimeError(f"Erro ao executar gdal_merge.py para {raster}")
            else:
                print(f"Mosaico parcial {output_file} criado com sucesso!")

            # Atualiza o mosaico temporário para o próximo ciclo
            temp_mosaic = output_file

    return temp_mosaic  # Retorna o último mosaico parcial gerado

# Função para renomear o mosaico final
def renomear_mosaico_final(result_folder, final_mosaic):
    # Nome do arquivo final
    output_file_final = os.path.join(result_folder, "mosaic_final.tif")

    # Renomear o arquivo final
    os.rename(final_mosaic, output_file_final)
    print(f"Mosaico final renomeado para: {output_file_final}")

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
    verificar_diretorio(raster_folder)
    demList = listar_arquivos_tif(raster_folder)

    # Criar o diretório de resultados, se não existir
    os.makedirs(result_folder, exist_ok=True)

    # Mosaicar em partes (um por vez) e obter o mosaico final
    final_mosaic = mosaicar_em_partes(result_folder, demList)

    # Renomear o mosaico final
    renomear_mosaico_final(result_folder, final_mosaic)

if __name__ == "__main__":
    main()

