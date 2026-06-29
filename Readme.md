# Programação Linear - Trabalho Final

Trabalho final desenvolvido para a disciplina de Programação Linear, com foco na modelagem e resolução de um problema de otimização relacionado à localização de centros de distribuição.

O projeto utiliza Python e o solver Gurobi para resolver cenários de escolha estratégica de localidades, considerando distância, demanda de entregas e equilíbrio operacional entre centros.

## Sobre o projeto

Uma empresa deseja instalar centros de distribuição para atender um conjunto de localidades.

Cada localidade possui coordenadas cartesianas, uma quantidade estimada de entregas semanais e uma indicação de elegibilidade para receber um centro de distribuição.

A partir desses dados, o objetivo é definir quais localidades devem ser escolhidas como centros, respeitando as restrições do problema e otimizando os critérios definidos.

## Objetivos

O trabalho foi dividido em dois cenários principais:

### Item A - Minimização da distância total

Escolher as localidades para instalação dos centros de distribuição de forma a minimizar a distância total percorrida para atender as cidades.

### Item B - Balanceamento entre centros

Escolher as localidades de forma que as distâncias percorridas pelos veículos sejam mais equilibradas entre os centros de distribuição.

Nesse cenário, o objetivo é reduzir a diferença entre as maiores e menores distâncias percorridas.

## Premissas do problema

- As localidades são representadas por coordenadas cartesianas.
- A distância entre localidades é calculada por distância euclidiana.
- A quantidade de entregas semanais influencia diretamente o custo/distância de atendimento.
- Apenas algumas localidades são candidatas a receber centros de distribuição.
- O número de centros a serem instalados é informado nos arquivos de entrada.

## Dados de entrada

Os arquivos de entrada estão disponíveis na pasta `Dados/`.

Cada arquivo representa uma instância do problema e segue a estrutura:

```text
Primeira linha: número de cidades
Segunda linha: número de centros de distribuição a serem instalados
Demais linhas:
  - coordenada x da cidade
  - coordenada y da cidade
  - número de entregas semanais
  - indicação se a cidade pode ser centro de distribuição
```

Arquivos disponíveis:

```text
inst_20_3.txt
inst_20_4.txt
inst_30_4.txt
inst_40_8.txt
inst_40_9.txt
inst_50_7.txt
inst_50_10.txt
inst_60_11.txt
inst_60_12.txt
```

## Tecnologias utilizadas

- Python
- Gurobi Optimizer
- NumPy
- Matplotlib

## Estrutura do repositório

```text
trabalho_final_prog_lin/
├── Dados/
│   ├── inst_20_3.txt
│   ├── inst_20_4.txt
│   ├── inst_30_4.txt
│   ├── inst_40_8.txt
│   ├── inst_40_9.txt
│   ├── inst_50_7.txt
│   ├── inst_50_10.txt
│   ├── inst_60_11.txt
│   └── inst_60_12.txt
├── scripts/
│   ├── script_a.py
│   └── script_b.py
├── Programação_Linear.pdf
├── requirements.txt
└── Readme.md
```

## Relatório

O arquivo `Programação_Linear.pdf` contém o relatório completo do trabalho, incluindo:

- descrição do problema;
- formulação matemática;
- definição das variáveis de decisão;
- função objetivo;
- restrições;
- experimentos computacionais;
- resultados obtidos;
- análise crítica;
- conclusão.

## Como executar

### Pré-requisitos

Para executar os scripts, é necessário ter:

- Python 3.8 ou superior;
- Gurobi Optimizer instalado;
- licença ativa do Gurobi;
- dependências listadas em `requirements.txt`.

### Clonar o repositório

```bash
git clone https://github.com/carolinakoike/trabalho_final_prog_lin.git
```

```bash
cd trabalho_final_prog_lin
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar os scripts

Para resolver o cenário do Item A:

```bash
python scripts/script_a.py
```

Para resolver o cenário do Item B:

```bash
python scripts/script_b.py
```

## Alterando a instância de entrada

Os scripts utilizam os arquivos disponíveis na pasta `Dados/`.

Para testar outra instância, altere no script o caminho do arquivo de entrada, por exemplo:

```python
arquivo = "Dados/inst_20_3.txt"
```

ou:

```python
arquivo = "Dados/inst_60_12.txt"
```

## Observação sobre o Gurobi

Este projeto utiliza o Gurobi como solver de otimização.

Para executar os scripts corretamente, é necessário ter o Gurobi instalado e configurado na máquina, além de uma licença válida.

## Status do projeto

Projeto acadêmico concluído.

O repositório foi mantido como registro de estudo em Programação Linear, modelagem matemática, otimização e uso de ferramentas computacionais para resolução de problemas reais.

## Aprendizados

Durante o desenvolvimento deste trabalho, foram praticados conceitos como:

- modelagem de problemas de otimização;
- programação linear;
- definição de variáveis de decisão;
- construção de função objetivo;
- elaboração de restrições;
- uso do solver Gurobi;
- leitura e tratamento de dados de entrada;
- análise de resultados computacionais.
