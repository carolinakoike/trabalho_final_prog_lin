import numpy as np
from gurobipy import Model, GRB

# Função para ler o arquivo e extrair coordenadas e informações
def ler_dados_instancia(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()
    
    num_cidades = int(linhas[0].strip())
    num_centros = int(linhas[1].strip())
    print(num_cidades, num_centros)
    
    # Armazenar coordenadas, número de entregas e elegibilidade como centro de distribuição
    coordenadas = []
    entregas = []
    elegivel_centro = []
    
    for linha in linhas[2:]:
        dados = linha.split()
        x, y = int(dados[0]), int(dados[1])
        num_entregas = int(dados[2])
        pode_ser_centro = int(dados[3])
        
        coordenadas.append((x, y))
        entregas.append(num_entregas)
        elegivel_centro.append(pode_ser_centro)
        
    return num_cidades, num_centros, coordenadas, entregas, elegivel_centro

# Calcula a distância euclidiana entre todas as localidades
def calcular_distancias(coordenadas):
    num_cidades = len(coordenadas)
    distancias = np.zeros((num_cidades, num_cidades))
    
    for i in range(num_cidades):
        for j in range(num_cidades):
            distancias[i, j] = np.sqrt((coordenadas[i][0] - coordenadas[j][0])**2 + (coordenadas[i][1] - coordenadas[j][1])**2)
    
    return distancias

# Carrega os dados
caminho_arquivo = 'Dados/inst_20_3.txt'  # substitua pelo caminho do arquivo
num_cidades, num_centros, coordenadas, entregas, elegivel_centro = ler_dados_instancia(caminho_arquivo)
distancias = calcular_distancias(coordenadas)
