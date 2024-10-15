#!/usr/bin/env python3
"""
Script de Mosaico de Rasters com GDAL e Python

Este script automatiza o processo de mosaico de arquivos raster (formato .tif) utilizando a biblioteca GDAL.
Ele permite processar arquivos raster grandes em partes, utilizando paralelismo para melhorar o desempenho e
compressão para otimizar o espaço de armazenamento.

### Funcionalidades:
1. Verifica se o diretório contendo os rasters de entrada existe e lista todos os arquivos .tif.
2. Mosaica dois rasters de cada vez para criar arquivos parciais (mosaicos intermediários).
3. Combina os mosaicos parciais em um mosaico final completo.
4. Utiliza `gdalwarp` para paralelizar o processamento e aplicar compressão DEFLATE.
5. Opções configuráveis de resolução espacial e sistema de referência (EPSG:4326 por padrão).

### Parâmetros:
- `raster_folder`: Diretório contendo os arquivos raster (.tif).
- `result_folder`: Diretório onde os arquivos de mosaico (parciais e final) serão salvos.

### Como usar:
1. Execute o script na linha de comando passando os diretórios de entrada e saída:
    ```
    python mosaic.py <caminho_para_raster_folder> <caminho_para_result_folder>
    ```

2. O script processará os rasters, criando mosaicos parciais e, por fim, um mosaico completo no diretório de saída.

### Requisitos:
- GDAL instalado com suporte para `gdalwarp` e `gdal_merge`.
- Bibliotecas: os, sys, subprocess, glob

### Exemplo:
    python mosaic.py ./raster_folder ./result_folder

Autor: Lucas Vasconcelos Vieira
"""
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

# Função para mosaicar dois rasters de cada vez com gdalwarp
def mosaicar_em_partes(result_folder, demList):
    temp_mosaics = []
    
    # Mosaicar dois rasters de cada vez
    for i in range(0, len(demList), 2):
        parte_rasters = demList[i:i + 2]
        
        # Nome do arquivo de mosaico parcial
        output_file = os.path.join(result_folder, f"mosaic_parcial_{i//2}.tif")
        temp_mosaics.append(output_file)
        
        # Comando gdalwarp com paralelismo e compressão DEFLATE
        cmd = [
            "gdalwarp", "-multi", "-wo", "NUM_THREADS=ALL_CPUS", "-co", "COMPRESS=DEFLATE",
            "-tr", str(res), str(res), "-t_srs", "EPSG:4326", "-r", "near",
            "-overwrite"
        ] + parte_rasters + [output_file]

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
        "-tr", str(res), str(res), "-t_srs", "EPSG:4326", "-r", "near",
        "-overwrite"
    ] + temp_mosaics + [output_file_final]

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
# Função principal para capturar os argumentos da linha de comando