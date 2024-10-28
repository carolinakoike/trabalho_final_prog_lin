import numpy as np
from gurobipy import Model, GRB, quicksum
import matplotlib.pyplot as plt

# Dados do problema
num_cidades = 60
num_centros = 12

# Coordenadas, número de entregas e elegibilidade para ser centro
dados_cidades = [
(397, 131, 5, 1),
(486, 72, 7, 0),
(321, 171, 10, 0),
(442, 394, 9, 1),
(30, 216, 8, 1),
(337, 307, 10, 1),
(75, 467, 5, 1),
(53, 196, 6, 0),
(51, 201, 2, 1),
(247, 271, 2, 1),
(133, 24, 4, 1),
(365, 55, 7, 0),
(364, 51, 2, 1),
(327, 420, 5, 0),
(172, 401, 8, 1),
(396, 124, 9, 1),
(174, 248, 3, 1),
(429, 213, 5, 1),
(318, 13, 8, 0),
(98, 249, 3, 0),
(75, 491, 2, 0),
(371, 239, 9, 1),
(136, 220, 7, 1),
(65, 70, 5, 0),
(186, 287, 5, 1),
(433, 121, 10, 0),
(350, 271, 9, 1),
(149, 293, 6, 0),
(371, 294, 7, 1),
(319, 486, 2, 0),
(14, 439, 8, 0),
(191, 11, 6, 0),
(342, 312, 9, 0),
(391, 146, 9, 0),
(290, 117, 7, 1),
(161, 362, 2, 1),
(368, 298, 5, 0),
(75, 498, 2, 0),
(463, 240, 7, 1),
(378, 328, 3, 1),
(94, 239, 4, 0),
(496, 375, 4, 1),
(37, 289, 8, 0),
(347, 241, 4, 1),
(70, 433, 10, 1),
(316, 370, 7, 1),
(156, 479, 6, 1),
(1, 4, 10, 1),
(108, 236, 4, 0),
(431, 386, 7, 1),
(386, 169, 6, 1),
(412, 294, 8, 1),
(139, 54, 10, 1),
(154, 232, 4, 1),
(420, 151, 8, 1),
(470, 341, 7, 1),
(222, 219, 3, 0),
(161, 292, 2, 1),
(66, 118, 10, 1),
(107, 356, 10, 0)
]

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
modelo1 = Model("Distribuicao")

# Variáveis de decisão
x = modelo1.addVars(num_cidades, num_cidades, vtype=GRB.BINARY, name="x")
y = modelo1.addVars(num_cidades, vtype=GRB.BINARY, name="y")

# Função objetivo: minimizar a soma das distâncias multiplicadas pelo número de entregas
modelo1.setObjective(
    quicksum(distancias[i][j] * entregas[j] * x[i, j] for i in range(num_cidades) for j in range(num_cidades)),
    GRB.MINIMIZE
)

# Restrição 1: cada cidade é atendida por exatamente um centro
for j in range(num_cidades):
    modelo1.addConstr(quicksum(x[i, j] for i in range(num_cidades)) == 1, f"Atendimento_{j}")

# Restrição 2: exatamente 12 centros de distribuição devem ser selecionados
modelo1.addConstr(quicksum(y[i] for i in range(num_cidades)) == num_centros, "Limite_Centros")

# Restrição 3: somente cidades elegíveis podem ser centros de distribuição
for i in range(num_cidades):
    if elegivel_centro[i] == 0:
        modelo1.addConstr(y[i] == 0, f"Elegibilidade_{i}")

# Restrição 4: uma cidade só pode atender outra se for um centro de distribuição
for i in range(num_cidades):
    for j in range(num_cidades):
        modelo1.addConstr(x[i, j] <= y[i], f"Centro_Atendimento_{i}_{j}")

# Suprimindo o output do terminal
modelo1.setParam("OutputFlag", 0)
    
# Executa a otimização
modelo1.optimize()

# Exibe resultados
if modelo1.status == GRB.OPTIMAL:
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
    
    # Exibição dos resultados no formato desejado
    print("Associação das cidades aos centros:")
    for idx, (centro, cidades_atendidas) in enumerate(atendimento_por_centro.items(), start=1):
        cidades_str = ", ".join(map(str, cidades_atendidas))
        print(f"  {idx}. Centro {centro} atende as cidades: {cidades_str}")

else:
    print("Não foi possível encontrar uma solução ótima.")

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

# Chamando a função para plotar o gráfico, caso o modelo1 encontre uma solução ótima
if modelo1.status == GRB.OPTIMAL:
    plot_distribuicao(coordenadas, centros_selecionados, atendimento_por_centro)


modelo2 = Model("Distribuicao_Equilibrada")

# Variáveis de decisão
x = modelo2.addVars(num_cidades, num_cidades, vtype=GRB.BINARY, name="x")
y = modelo2.addVars(num_cidades, vtype=GRB.BINARY, name="y")

# Variáveis para distâncias percorridas por cada centro, e para a distância máxima e mínima
distancia_centro = modelo2.addVars(num_cidades, vtype=GRB.CONTINUOUS, name="distancia_centro")
max_dist = modelo2.addVar(vtype=GRB.CONTINUOUS, name="max_dist")
min_dist = modelo2.addVar(vtype=GRB.CONTINUOUS, name="min_dist")

# Função objetivo: minimizar a diferença entre a distância máxima e mínima percorrida pelos centros
modelo2.setObjective(max_dist - min_dist, GRB.MINIMIZE)

# Restrição 1: cada cidade é atendida por exatamente um centro
for j in range(num_cidades):
    modelo2.addConstr(quicksum(x[i, j] for i in range(num_cidades)) == 1, f"Atendimento_{j}")

# Restrição 2: exatamente 12 centros de distribuição devem ser selecionados
modelo2.addConstr(quicksum(y[i] for i in range(num_cidades)) == num_centros, "Limite_Centros")

# Restrição 3: somente cidades elegíveis podem ser centros de distribuição
for i in range(num_cidades):
    if elegivel_centro[i] == 0:
        modelo2.addConstr(y[i] == 0, f"Elegibilidade_{i}")

# Restrição 4: uma cidade só pode atender outra se for um centro de distribuição
for i in range(num_cidades):
    for j in range(num_cidades):
        modelo2.addConstr(x[i, j] <= y[i], f"Centro_Atendimento_{i}_{j}")

# Restrição 5: definir a distância total percorrida por cada centro
for i in range(num_cidades):
    modelo2.addConstr(distancia_centro[i] == quicksum(distancias[i][j] * entregas[j] * x[i, j] for j in range(num_cidades)), f"Distancia_Centro_{i}")

# Restrição 6: a distância percorrida por cada centro deve estar entre min_dist e max_dist
for i in range(num_cidades):
    modelo2.addConstr(distancia_centro[i] <= max_dist, f"Distancia_Maxima_{i}")
    modelo2.addConstr(distancia_centro[i] >= min_dist, f"Distancia_Minima_{i}")

# Suprimindo o output do terminal
modelo2.setParam("OutputFlag", 0)

# Executa a otimização
modelo2.optimize()

# Exibe resultados
if modelo2.status == GRB.OPTIMAL:
    centros_selecionados = [i for i in range(num_cidades) if y[i].X > 0.5]
    print(f"Centros selecionados: {centros_selecionados}")
    
    # Exibe as distâncias percorridas e o balanceamento entre elas
    distancia_total_centros = {i: distancia_centro[i].X for i in centros_selecionados}
    max_dist_val = max_dist.X
    min_dist_val = min_dist.X
    print(f"Distância máxima percorrida: {max_dist_val:.2f}")
    print(f"Distância mínima percorrida: {min_dist_val:.2f}")
    print(f"Diferença entre distâncias: {max_dist_val - min_dist_val:.2f}")

    # Exibição das cidades atendidas por cada centro
    atendimento_por_centro = {centro: [] for centro in centros_selecionados}
    for j in range(num_cidades):
        for i in centros_selecionados:
            if x[i, j].X > 0.5:
                atendimento_por_centro[i].append(j)
                break
    
    print("\nAssociação das cidades aos centros:")
    for idx, (centro, cidades_atendidas) in enumerate(atendimento_por_centro.items(), start=1):
        cidades_str = ", ".join(map(str, cidades_atendidas))
        print(f"  {idx}. Centro {centro} atende as cidades: {cidades_str}")
else:
    print("Não foi possível encontrar uma solução ótima.")

if modelo2.status == GRB.OPTIMAL:
    plot_distribuicao(coordenadas, centros_selecionados, atendimento_por_centro)
