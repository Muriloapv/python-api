from pyDatalog import pyDatalog

# Inicializando o pyDatalog
pyDatalog.clear()

# Definindo os termos
pyDatalog.create_terms('Funcionario, Departamento, Projeto, TrabalhaEm, DepartamentoLotado')
pyDatalog.create_terms('D, F, P, Capacidade, FuncionarioEmProjeto, QtdFunc, qtd, capacidade')

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

# Carregar dados dos arquivos
carregar_dados()

# Definindo predicado que relaciona funcionários únicos com departamentos baseados no projeto
FuncionarioEmProjeto(D, F) <= (TrabalhaEm(F, P) & Projeto(P, D))

# Contando funcionários únicos por departamento e adicionando diretamente a `QtdFunc` como fato
departamentos = {}  # Definindo o dicionário 'departamentos' globalmente para uso posterior
for d in Departamento(D, Capacidade).data:
    dept = d[0]
    capacidade = d[1]
    # Contar funcionários únicos alocados em projetos para cada departamento
    funcionarios_unicos = set([f[0] for f in FuncionarioEmProjeto(dept, F).data])
    qtd_funcionarios = len(funcionarios_unicos)
    + QtdFunc(dept, qtd_funcionarios)
    + Departamento(dept, capacidade)
    # Adicionando ao dicionário 'departamentos' para uso posterior
    departamentos[dept] = {'capacidade': capacidade, 'qtd_funcionarios': qtd_funcionarios}

# Ajuste no predicado `DepartamentoLotado` para verificar se há funcionários alocados e se a contagem atinge a capacidade
DepartamentoLotado(D) <= (QtdFunc(D, qtd) & Departamento(D, capacidade) & (qtd > 0) & (qtd >= capacidade))

# Verificando e imprimindo quais departamentos estão lotados
print("Departamentos com funcionários alocados e verificação de lotação:")
for dept, info in departamentos.items():
    lotado = DepartamentoLotado(dept) != ()
    print(f"Departamento: {dept}, Funcionários Alocados: {info['qtd_funcionarios']}, Lotado: {lotado}")

# Exibindo funcionários em departamentos que não estão lotados
print("\nFuncionários em departamentos que não estão lotados:")
for dept, info in departamentos.items():
    if DepartamentoLotado(dept) == ():
        funcionarios = list(set([f[0] for f in FuncionarioEmProjeto(dept, F).data]))
        print(f"Departamento: {dept}, Funcionários: {funcionarios}")
