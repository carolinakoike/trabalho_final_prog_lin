import numpy as np
from gurobipy import Model, GRB, quicksum
import os

# Caminho para a pasta onde estão os arquivos de dados
caminho_pasta_dados = 'Dados'

# Lista de arquivos na pasta Dados
arquivos_instancias = [os.path.join(caminho_pasta_dados, arquivo) for arquivo in os.listdir(caminho_pasta_dados) if arquivo.endswith('.txt')]

# Função para ler o arquivo e extrair coordenadas e informações
def ler_dados_instancia(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()
    
    num_cidades = int(linhas[0].strip())
    num_centros = int(linhas[1].strip())
    
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

# Lista para armazenar os resultados
resultados = []

# Processa cada arquivo na pasta Dados
for caminho_arquivo in arquivos_instancias:
    print(f"Processando {caminho_arquivo}...")
    
    # Carregar dados da instância
    num_cidades, num_centros, coordenadas, entregas, elegivel_centro = ler_dados_instancia(caminho_arquivo)
    distancias = calcular_distancias(coordenadas)
    
    # Criação do modelo de otimização
    modelo = Model("Distribuicao")

    # Suprimindo o output do terminal
    modelo.setParam("OutputFlag", 0)
    
    # Variáveis de decisão
    x = modelo.addVars(num_cidades, num_cidades, vtype=GRB.BINARY, name="x")
    y = modelo.addVars(num_cidades, vtype=GRB.BINARY, name="y")

    # Função objetivo: minimizar a soma das distâncias multiplicadas pelo número de entregas
    modelo.setObjective(
        quicksum(distancias[i][j] * entregas[j] * x[i, j] for i in range(num_cidades) for j in range(num_cidades)),
        GRB.MINIMIZE
    )

    # Restrição 1: cada cidade é atendida por exatamente um centro
    for j in range(num_cidades):
        modelo.addConstr(quicksum(x[i, j] for i in range(num_cidades)) == 1, f"Atendimento_{j}")

    # Restrição 2: limite de centros de distribuição a serem criados
    modelo.addConstr(quicksum(y[i] for i in range(num_cidades)) == num_centros, "Limite_Centros")

    # Restrição 3: somente cidades elegíveis podem ser centros de distribuição
    for i in range(num_cidades):
        if elegivel_centro[i] == 0:
            modelo.addConstr(y[i] == 0, f"Elegibilidade_{i}")
    
    # Restrição 4: uma cidade só pode atender outra se for um centro de distribuição
    for i in range(num_cidades):
        for j in range(num_cidades):
            modelo.addConstr(x[i, j] <= y[i], f"Centro_Atendimento_{i}_{j}")
            
    # Executa a otimização
    modelo.optimize()

    # Exibe resultados e armazena os dados
    if modelo.status == GRB.OPTIMAL:
        print(f"Solução ótima encontrada para {caminho_arquivo}")
        centros_selecionados = [i for i in range(num_cidades) if y[i].X > 0.5]
        
        # Total de distância percorrida
        distancia_total = sum(distancias[i][j] * entregas[j] * x[i, j].X for i in range(num_cidades) for j in range(num_cidades) if x[i, j].X > 0.5)
        print(f"Distância total percorrida: {distancia_total:.2f}")
        
        # Associação das cidades aos centros
        associacao = {}
        for j in range(num_cidades):
            for i in centros_selecionados:
                if x[i, j].X > 0.5:
                    associacao[j] = i
                    break
        
        print("Associação das cidades aos centros:")
        for cidade, centro in associacao.items():
            print(f"  Cidade {cidade} -> Centro {centro}")
        
        # Armazena o resultado da instância
        resultados.append({
            "instancia": caminho_arquivo,
            "distancia_total": distancia_total,
            "centros_selecionados": centros_selecionados
        })
    else:
        print(f"Não foi possível encontrar uma solução ótima para {caminho_arquivo}")

# Exibe um resumo dos resultados após a execução de todas as instâncias
print("\nResumo dos Resultados:")
for resultado in resultados:
    print(f"Instância: {resultado['instancia']}")
    print(f"  Distância Total: {resultado['distancia_total']}")
    print(f"  Centros Selecionados: {resultado['centros_selecionados']}\n")
