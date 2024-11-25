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

Uma empresa deseja instalar \(m\) centros de distribuição para atender \(n\) localidades representadas por \(L1, L2, ..., Ln\). Cada localidade possui uma quantidade estimada de entregas semanais, e algumas localidades são candidatas a abrigar os centros.

### Objetivos

- **Item (a):** Escolher localidades que minimizem a distância total percorrida para as entregas semanais.
- **Item (b):** Escolher localidades de forma que as distâncias percorridas pelos veículos sejam equilibradas entre os centros.

### Premissas
- A distância entre as localidades é calculada utilizando a **distância euclidiana**.
- O número de entregas semanais influencia diretamente as distâncias percorridas.

### Dados do Problema

- **Primeira Linha:** Número de cidades.
- **Segunda Linha:** Número de centros de distribuição a serem criados.
- **Primeira e Segunda Colunas:** Coordenadas cartesianas de cada cidade \(x, y\).
- **Terceira Coluna:** Número de entregas em cada cidade.
- **Quarta Coluna:** Indica se a cidade pode (1) ou não (0) ser centro de distribuição.

## Organização do Repositório

O repositório contém os seguintes arquivos e diretórios:

- `dados/`: Arquivos contendo os dados de entrada para os diferentes cenários.
- `scripts/`: Implementação dos modelos de programação linear em Python, utilizando o solver Gurobi.
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
   ```

2. Configuração dos Arquivos de Dados
Os arquivos de dados utilizados para resolver o problema estão localizados na pasta 'dados/'. Para executar o script com um arquivo específico, é necessário alterar o nome do arquivo na linha 22 do script principal:

   ```bash
   arquivo = 'dados/inst_60_12.txt'  # Caminho do arquivo
   ```
   Passos para usar um arquivo diferente:
   Abra o script Python no editor de sua preferência.
   Localize a linha 22.
   Substitua 'dados/inst_60_12.txt' pelo caminho relativo ao arquivo de dados desejado. Por exemplo:
   Para o arquivo inst_20_3.txt:
      ```bash
      arquivo = 'dados/inst_20_3.txt'
      ```

   Para o arquivo inst_50_7.txt:
      ```bash
      arquivo = 'dados/inst_50_7.txt'
      ```
      
   Arquivos disponíveis:
   - 'inst_20_3.txt'
   - 'inst_20_4.txt'
   - 'inst_30_4.txt'
   - 'inst_40_8.txt'
   - 'inst_40_9.txt'
   - 'inst_50_7.txt'
   - 'inst_50_10.txt'
   - 'inst_60_11.txt'
   - 'inst_60_12.txt'