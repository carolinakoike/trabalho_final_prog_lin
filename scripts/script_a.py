import numpy as np
from gurobipy import Model, GRB, quicksum
import matplotlib.pyplot as plt

# Função para ler os dados do arquivo
def ler_dados(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    
    # Primeira linha: número de cidades
    num_cidades = int(linhas[0].strip())
    # Segunda linha: número de centros de distribuição
    num_centros = int(linhas[1].strip())
    # Linhas seguintes: coordenadas, número de entregas e elegibilidade
    dados_cidades = []
    for linha in linhas[2:]:
        x, y, entregas, elegivel = map(int, linha.split())
        dados_cidades.append((x, y, entregas, elegivel))
    return num_cidades, num_centros, dados_cidades

# Ler os dados do arquivo
arquivo = 'dados/inst_60_12.txt'  # Caminho do arquivo
num_cidades, num_centros, dados_cidades = ler_dados(arquivo)

# Extrair coordenadas, número de entregas e elegibilidade
coordenadas = [(x, y) for x, y, _, _ in dados_cidades]
entregas = [num_entregas for _, _, num_entregas, _ in dados_cidades]
elegivel_centro = [pode_ser_centro for _, _, _, pode_ser_centro in dados_cidades]

# Calcular distâncias euclidianas entre todas as cidades
distancias = np.zeros((num_cidades, num_cidades))
for i in range(num_cidades):
    for j in range(num_cidades):
        distancias[i, j] = np.sqrt((coordenadas[i][0] - coordenadas[j][0])**2 + (coordenadas[i][1] - coordenadas[j][1])**2)

# Modelo de otimização
modelo = Model("Distribuicao")

# Variáveis de decisão
x = modelo.addVars(num_cidades, num_cidades, vtype=GRB.BINARY, name="x")
y = modelo.addVars(num_cidades, vtype=GRB.BINARY, name="y")

# Função objetivo: minimizar a soma das distâncias multiplicadas pelo número de entregas
modelo.setObjective(
    quicksum(distancias[i][j] * entregas[j] * x[i, j] for i in range(num_cidades) for j in range(num_cidades)),
    GRB.MINIMIZE
)

# Restrições
# Restrição 1: cada cidade é atendida por exatamente um centro
for j in range(num_cidades):
    modelo.addConstr(quicksum(x[i, j] for i in range(num_cidades)) == 1, f"Atendimento_{j}")

# Restrição 2: exatamente 'num_centros' centros de distribuição devem ser selecionados
modelo.addConstr(quicksum(y[i] for i in range(num_cidades)) == num_centros, "Limite_Centros")

# Restrição 3: somente cidades elegíveis podem ser centros de distribuição
for i in range(num_cidades):
    if elegivel_centro[i] == 0:
        modelo.addConstr(y[i] == 0, f"Elegibilidade_{i}")

# Restrição 4: uma cidade só pode atender outra se for um centro de distribuição
for i in range(num_cidades):
    for j in range(num_cidades):
        modelo.addConstr(x[i, j] <= y[i], f"Centro_Atendimento_{i}_{j}")

# Suprimindo o output do terminal
# modelo.setParam("OutputFlag", 0)
    
# Executa a otimização
modelo.optimize()

# Exibe os resultados
if modelo.status == GRB.OPTIMAL:
    centros_selecionados = [i for i in range(num_cidades) if y[i].X > 0.5]
    print(f"Centros selecionados: {centros_selecionados}")
    
    distancia_total = sum(distancias[i][j] * entregas[j] * x[i, j].X for i in range(num_cidades) for j in range(num_cidades) if x[i, j].X > 0.5)
    print(f"Distância total percorrida: {distancia_total:.2f}")
    
    # Organização das cidades atendidas por cada centro
    atendimento_por_centro = {centro: [] for centro in centros_selecionados}
    for j in range(num_cidades):
        for i in centros_selecionados:
            if x[i, j].X > 0.5:
                atendimento_por_centro[i].append(j)
                break
    
    # Calcular a maior e menor distância entre os centros e as cidades atendidas
    maior_distancia = 0
    menor_distancia = float('inf')
    centro_maior, cidade_maior = None, None
    centro_menor, cidade_menor = None, None

    # Adicionar cálculos para a maior e menor distância ponderada
    maior_distancia_ponderada = 0
    menor_distancia_ponderada = float('inf')
    centro_maior_ponderada, cidade_maior_ponderada = None, None
    centro_menor_ponderada, cidade_menor_ponderada = None, None

    distancia_total_centros = {}  # Dicionário para armazenar as distâncias totais por centro

    # Ajuste para ignorar distâncias entre uma cidade e ela mesma
    for centro, cidades in atendimento_por_centro.items():
        total_distancia_centro = 0  # Inicializar a distância total de cada centro
        for cidade in cidades:
            if centro != cidade:  # Ignorar a distância de uma cidade para ela mesma
                distancia = distancias[centro, cidade]
                distancia_ponderada = distancia * entregas[cidade]
                total_distancia_centro += distancia_ponderada
                # Atualizar maior e menor distância simples
                if distancia > maior_distancia:
                    maior_distancia = distancia
                    centro_maior, cidade_maior = centro, cidade
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    centro_menor, cidade_menor = centro, cidade
                # Atualizar maior e menor distância ponderada
                if distancia_ponderada > maior_distancia_ponderada:
                    maior_distancia_ponderada = distancia_ponderada
                    centro_maior_ponderada, cidade_maior_ponderada = centro, cidade
                if distancia_ponderada < menor_distancia_ponderada:
                    menor_distancia_ponderada = distancia_ponderada
                    centro_menor_ponderada, cidade_menor_ponderada = centro, cidade
        # Armazenar a distância total percorrida pelo centro
        distancia_total_centros[centro] = total_distancia_centro

    # Exibir os resultados
    print(f"Maior distância entre um centro e uma cidade: {maior_distancia:.2f} (Centro {centro_maior} para Cidade {cidade_maior})")
    print(f"Menor distância entre um centro e uma cidade: {menor_distancia:.2f} (Centro {centro_menor} para Cidade {cidade_menor})")
    print(f"Maior distância ponderada (com número de viagens): {maior_distancia_ponderada:.2f} (Centro {centro_maior_ponderada} para Cidade {cidade_maior_ponderada})")
    print(f"Menor distância ponderada (com número de viagens): {menor_distancia_ponderada:.2f} (Centro {centro_menor_ponderada} para Cidade {cidade_menor_ponderada})")
    print("\nDistância total percorrida por cada centro de distribuição:")
    for centro, total_distancia in distancia_total_centros.items():
        print(f"  Centro {centro}: {total_distancia:.2f}")

    # Exibição dos resultados no formato desejado
    print("\nAssociação das cidades aos centros:")
    for idx, (centro, cidades_atendidas) in enumerate(atendimento_por_centro.items(), start=1):
        cidades_str = ", ".join(map(str, cidades_atendidas))
        print(f"  {idx}. Centro {centro} atende as cidades: {cidades_str}")

    # Função para plotar o gráfico das cidades e centros de distribuição
    def plot_distribuicao(coordenadas, centros_selecionados, atendimento_por_centro):
        plt.figure(figsize=(10, 8))

        # Plotar todas as cidades
        for idx, (x, y) in enumerate(coordenadas):
            plt.plot(x, y, 'bo', markersize=5)  # Pontos das cidades em azul
            plt.text(x, y, str(idx), fontsize=8, ha='right')  # Identificadores das cidades
        
        # Destacar os centros de distribuição
        for centro in centros_selecionados:
            plt.plot(coordenadas[centro][0], coordenadas[centro][1], 'ro', markersize=8)  # Centros em vermelho
            plt.text(coordenadas[centro][0], coordenadas[centro][1], f"C{centro}", fontsize=10, ha='left', color='red')

        # Traçar linhas entre cada cidade e seu centro de distribuição
        for centro, cidades_atendidas in atendimento_por_centro.items():
            for cidade in cidades_atendidas:
                x_values = [coordenadas[cidade][0], coordenadas[centro][0]]
                y_values = [coordenadas[cidade][1], coordenadas[centro][1]]
                plt.plot(x_values, y_values, 'g--', linewidth=0.8)  # Linhas em tracejado verde

        plt.xlabel('Coordenada X')
        plt.ylabel('Coordenada Y')
        plt.title('Distribuição de Centros e Cidades Atendidas')
        plt.grid(True)
        plt.show()

    # Chamando a função para plotar o gráfico
    plot_distribuicao(coordenadas, centros_selecionados, atendimento_por_centro)
else:
    print("Não foi possível encontrar uma solução ótima.")
