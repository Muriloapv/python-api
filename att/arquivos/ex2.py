from pyDatalog import pyDatalog

# Inicializando o pyDatalog
pyDatalog.clear()

# Definindo os termos
pyDatalog.create_terms('Funcionario, Departamento, Projeto, TrabalhaEm, ProjetoCompartilhado')
pyDatalog.create_terms('D, D1, D2, F, P, FuncionarioEmProjeto, pertenceA')

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
FuncionarioEmProjeto(D, F) <= (TrabalhaEm(F, P) & Projeto(P, D))

# Criar o predicado para identificar projetos compartilhados por diferentes departamentos
pertenceA(P, D) <= (TrabalhaEm(F, P) & Funcionario(F, D))  # Departamento de cada projeto

# Projeto é compartilhado se existir mais de um departamento associado a ele
ProjetoCompartilhado(P) <= (pertenceA(P, D1) & pertenceA(P, D2) & (D1 != D2))

# Listar os projetos que são compartilhados entre departamentos
print("Projetos Compartilhados entre Departamentos:")
for projeto in ProjetoCompartilhado(P).data:
    print(f"Projeto: {projeto[0]}")

# Para cada projeto compartilhado, listar os funcionários e seus departamentos
print("\nFuncionários e Departamentos para Projetos Compartilhados:")
for projeto in ProjetoCompartilhado(P).data:
    nome_projeto = projeto[0]
    funcionarios = [(f[0], f[1]) for f in (TrabalhaEm(F, nome_projeto) & Funcionario(F, D)).data]
    print(f"\nProjeto: {nome_projeto}")
    for funcionario, dept in funcionarios:
        print(f"  Funcionário: {funcionario}, Departamento: {dept}")
