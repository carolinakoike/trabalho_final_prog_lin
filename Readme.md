# Programação Linear - Trabalho Final

Este repositório contém a modelagem, implementação e análise de um problema de otimização relacionado à localização de centros de distribuição. O projeto inclui o relatório completo e os scripts de programação utilizados.

## Descrição do Trabalho

O objetivo do trabalho é resolver um problema de otimização utilizando programação linear. O estudo foca na escolha estratégica de localidades para instalação de centros de distribuição, considerando dois cenários principais:

1. **Minimização das distâncias totais percorridas** para atender as cidades.
2. **Equilíbrio entre as distâncias percorridas** pelos centros de distribuição, minimizando a diferença entre as maiores e menores distâncias percorridas.

O relatório inclui:
- Apresentação detalhada do problema.
- Modelagem matemática, com definição das variáveis de decisão, função objetivo, restrições e parâmetros.
- Experimentos computacionais utilizando o solver Gurobi.
- Resultados obtidos e análise crítica.
- Conclusão e sugestões para trabalhos futuros.

## Problema

Uma empresa deseja instalar \(m\) centros de distribuição para atender \(n\) localidades representadas por \(L_1, L_2, \dots, L_n\). Cada localidade possui uma quantidade estimada de entregas semanais, e algumas localidades são candidatas a abrigar os centros.

### Objetivos

- **Item (a):** Escolher localidades que minimizem a distância total percorrida para as entregas semanais.
- **Item (b):** Escolher localidades de forma que as distâncias percorridas pelos veículos sejam equilibradas entre os centros.

### Premissas
- A distância entre as localidades é calculada utilizando a **distância euclidiana**.
- O número de entregas semanais influencia diretamente o custo das distâncias.

### Dados do Problema

- **Primeira Linha:** Número de cidades.
- **Segunda Linha:** Número de centros de distribuição a serem criados.
- **Primeira e Segunda Colunas:** Coordenadas cartesianas de cada cidade (\(x, y\)).
- **Terceira Coluna:** Número de entregas em cada cidade.
- **Quarta Coluna:** Indica se a cidade pode (1) ou não (0) ser centro de distribuição.

## Organização do Repositório

O repositório contém os seguintes arquivos e diretórios:

- `dados/`: Arquivos contendo os dados de entrada para os diferentes cenários.
- `scripts/`: Implementação dos modelos de programação linear em Python, utilizando o solver Gurobi.
- `resultados/`: Saídas geradas pelos experimentos computacionais.
- `relatorio/`: Documento completo em PDF, contendo a modelagem, resultados e conclusões.

## Requisitos

Para executar os scripts, é necessário:
- **Python 3.8 ou superior.**
- **Gurobi Solver** com licença ativa.
- Bibliotecas adicionais listadas no arquivo `requirements.txt`.

## Como Executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/carolinakoike/trabalho_final_prog_lin.git
