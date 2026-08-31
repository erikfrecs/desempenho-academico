def solve_academic_records():

    # Leitura dos arquivos
    with open("cenarios/02_desempenho_academico/dados/notas.csv", "r", encoding="utf-8") as arquivo:
        raw_notas = arquivo.read()

    with open("cenarios/02_desempenho_academico/dados/matriculas.csv", "r", encoding="utf-8") as arquivo:
        raw_matriculas = arquivo.read()

    # Limpeza de Dados: Uso de "set" para eliminar os registros duplicados
    linhas = raw_notas.strip().split('\n')[1:]
    registros_unicos = set(linhas)

    # Modelagem: Lista de Dicionários convertendo os tipos corretos
    dados = []
    for linha in registros_unicos:
        partes = linha.split(',')
        dados.append({
            'id': partes[0],
            'aluno': partes[1],
            'disciplina': partes[2],
            'nota': float(partes[3]),
            'frequencia': int(partes[4]),
            'atividades': int(partes[5])
        })

    # FUNÇÃO 1: Análise de Desempenho
    def analisar_desempenho_disciplinas(dados):
        disciplinas = set([d['disciplina'] for d in dados])

        analise = {disc: {'soma_notas': 0, 'count': 0, 'alunos': {}} for disc in disciplinas}

        for d in dados:
            disc = d['disciplina']
            aluno = d['aluno']
            analise[disc]['soma_notas'] += d['nota']
            analise[disc]['count'] += 1

            if aluno not in analise[disc]['alunos']:
                analise[disc]['alunos'][aluno] = []

            analise[disc]['alunos'][aluno].append(d['nota'])

        resultados = {}

        for disc, info in analise.items():
            media_geral = info['soma_notas'] / info['count']

            medias_alunos = [(aluno, sum(notas)/len(notas)) for aluno, notas in info['alunos'].items()]
            melhor_aluno = max(medias_alunos, key=lambda x: x[1])

            resultados[disc] = {'media': media_geral, 'melhor_aluno': melhor_aluno}

        return resultados

    # FUNÇÃO 2: Filtro de Alunos em Risco
    def encontrar_alunos_risco(dados):
        risco = [d for d in dados if d['nota'] < 6.0 or d['frequencia'] < 75]
        return risco

    # FUNÇÃO 3: Operações de Conjuntos para cruzamento de matrículas
    def analise_matriculas(raw_matriculas):
        linhas_matriculas = raw_matriculas.strip().split('\n')
        matriculas_unicas = set(linhas_matriculas)

        # Tupla: aluno e disciplina
        matriculas = []
        for linha in matriculas_unicas:
            partes = linha.split(',')
            matriculas.append((partes[0], partes[1]))

        aluno_disc = {}

        for aluno, disciplina in matriculas:
            if aluno not in aluno_disc:
                aluno_disc[aluno] = set()

            aluno_disc[aluno].add(disciplina)

        multidisciplinares = [aluno for aluno, discs in aluno_disc.items() if len(discs) >= 2]

        alunos_algoritmos = {aluno for aluno, discs in aluno_disc.items() if 'Algoritmos' in discs}
        alunos_python = {aluno for aluno, discs in aluno_disc.items() if 'Python' in discs}

        ambas = alunos_algoritmos.intersection(alunos_python)
        apenas_algoritmos = alunos_algoritmos.difference(alunos_python)

        return multidisciplinares, ambas, apenas_algoritmos

    desempenho = analisar_desempenho_disciplinas(dados)
    risco = encontrar_alunos_risco(dados)
    multidisciplinares, ambas, apenas_alg = analise_matriculas(raw_matriculas)

    # Dict Comprehension
    medias_disciplinas = {disc: info['media'] for disc, info in desempenho.items()}

    print("=== ANÁLISE DE DESEMPENHO POR DISCIPLINA ===")

    for disc, info in desempenho.items():
        print(f"Disciplina: {disc}")
        print(f"  Média Geral: {info['media']:.2f}")
        print(f"  Melhor Aluno: {info['melhor_aluno'][0]} (Média: {info['melhor_aluno'][1]:.2f})\n")

    print("=== MÉDIAS DAS DISCIPLINAS ===")

    for disc, media in medias_disciplinas.items():
        print(f"{disc}: {media:.2f}")

    print("=== ALUNOS ABAIXO DOS CRITÉRIOS (RISCO) ===")
    print(f"Total de registros críticos (Nota < 6.0 ou Frequência < 75%): {len(risco)}")

    for r in risco:
        print(f"  {r['aluno']} | {r['disciplina']} | Nota: {r['nota']} | Freq: {r['frequencia']}%")

    print("\n=== ANÁLISE DE MATRÍCULAS (CONJUNTOS) ===")
    print(f"Alunos cursando 2 ou mais disciplinas: {len(multidisciplinares)} alunos")
    print(f"Alunos em Algoritmos E Python (Interseção): {', '.join(ambas)}")
    print(f"Alunos em Algoritmos, mas NÃO em Python (Diferença): {', '.join(apenas_alg)}")


if __name__ == "__main__":
    solve_academic_records()