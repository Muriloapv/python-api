from pyDatalog import pyDatalog

# Inicializando o pyDatalog
pyDatalog.clear()

# Definindo os termos
pyDatalog.create_terms('Funcionario, Departamento, Projeto, TrabalhaEm, ColegaDeProjeto')
pyDatalog.create_terms('X, Y, D1, D2, F, P')

# Função para carregar dados dos arquivos
def carregar_dados():
    # Lendo e carregando os departamentos e capacidades
    with open('departamentos.txt', 'r') as file:
        next(file)  # Ignora o cabeçalho
        for line in file:
            nome, capacidade = line.strip().split(';')
            + Departamento(nome, int(capacidade))

    # Lendo e carregando as alocações de funcionários em projetos
    with open('alocacoes.txt', 'r') as file:
        next(file)  # Ignora o cabeçalho
        for line in file:
            funcionario, projeto = line.strip().split(';')
            + TrabalhaEm(funcionario, projeto)

    # Lendo e carregando a associação de projetos com departamentos
    with open('projetos.txt', 'r') as file:
        next(file)  # Ignora o cabeçalho
        for line in file:
            projeto, dept_responsavel = line.strip().split(';')
            + Projeto(projeto, dept_responsavel)

    # Lendo os funcionários do arquivo funcionarios.txt e adicionando o fato `Funcionario`
    with open('funcionarios.txt', 'r') as file:
        next(file)  # Ignora o cabeçalho
        for line in file:
            nome, dept, experiencia = line.strip().split(';')
            + Funcionario(nome, dept)  # Define o fato `Funcionario` com o nome e o departamento

# Carregar dados dos arquivos
carregar_dados()

# Definindo predicado que relaciona funcionários com projetos e departamentos
ColegaDeProjeto(X, Y, P) <= (TrabalhaEm(X, P) & TrabalhaEm(Y, P) & Funcionario(X, D1) & Funcionario(Y, D2) & (D1 != D2) & (X != Y))

# Listar os pares de colegas de projeto e os projetos nos quais trabalham juntos
print("Pares de Funcionários Colegas de Projeto e seus respectivos Projetos:")
for colega in ColegaDeProjeto(X, Y, P).data:
    print(f"Funcionário: {colega[0]}, Colega: {colega[1]}, Projeto: {colega[2]}")

# Contar o número de colegas de projeto para cada funcionário
# Usar uma abordagem manual para contagem
print("\nContagem de Colegas de Projeto por Funcionário:")
colegas_count = {}
for colega in ColegaDeProjeto(X, Y, P).data:
    if colega[0] not in colegas_count:
        colegas_count[colega[0]] = set()
    colegas_count[colega[0]].add(colega[1])

for funcionario, colegas in colegas_count.items():
    print(f"Funcionário: {funcionario}, Número de Colegas de Projeto: {len(colegas)}")
