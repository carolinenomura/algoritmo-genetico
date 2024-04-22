import random
import math

def gerar_populacao(tam, min, max):
    """
    Gera uma população inicial de tamanho 'tam' com valores entre 'min' e 'max'.
    """
    populacao = []
    for x in range(tam):
        individuo = random.randint(min, max)
        populacao.append(individuo)
    return populacao

def avaliar_aptidao(x):
    """
    Avalia a aptidão de um indivíduo.
    """
    aptidao = (x ** 2) + (5 * x) - 5
    return aptidao

def calcular_probabilidade(x, soma_aptidao):
    """
    Calcula a probabilidade de seleção de um indivíduo com base em sua aptidão.
    """
    return (x * 100) / soma_aptidao

def selecao(populacao, numeros_roleta):
    """
    Seleciona indivíduos da população para evolução.
    """
    # Calcula a aptidao de cada individuo, adiciona na lista de aptidões e incrementa a soma
    aptidoes = []
    for individuo in populacao:
        aptidoes.append(avaliar_aptidao(individuo))
    soma_aptidao = sum(aptidoes)
    # Calcula a probabilidade de cada indivíduo ser escolhido baseada na aptidão
    probabilidades = []
    for aptidao in aptidoes:
        probabilidades.append(round(aptidao / soma_aptidao * 100))
    # Descobre quais indivíduos os números da roleta sortearam
    selecionados = []
    for num in numeros_roleta:
        lim_superior = 0
        for i, prob in enumerate(probabilidades):
            lim_superior += prob
            if num < lim_superior:
                selecionados.append(populacao[i])
                break
    return selecionados
    
def crossover(pai1, pai2):
    """
    Realiza o cruzamento entre dois pais em dois pontos de corte k, gerando dois filhos de cada par.
    """
    num_digitos = 8
    pontos_de_corte = [2]
    pai1_binario = format(pai1, f'0{num_digitos}b')
    pai2_binario = format(pai2, f'0{num_digitos}b')

    filho1 = pai1_binario[:2] + pai2_binario[2:4] + pai1_binario[4:]
    filho2 = pai2_binario[:2] + pai1_binario[2:4] + pai2_binario[4:]

    filhos = [int(filho1, 2), int(filho2, 2)]
    return filhos

def mutacao(individuo_int, prob_gerada, Pm):
    """
    Realiza a mutação em um indivíduo com base em probabilidades geradas.
    """
    individuo_mutado = []
    num_digitos = 8
    individuo = format(individuo_int, f'0{num_digitos}b')
    # Inverte bits que tiverem sua probabilidade gerada menor que a taxa de mutação Pm
    for i, bit in enumerate(individuo):
        if prob_gerada[i] <= Pm:
            if bit == '1':
                individuo_mutado.append('0')
            else:
                individuo_mutado.append('1')
        else:
            individuo_mutado.append(bit)
    # junta os caracteres de bits e reconverte de binário para inteiro
    individuo_mutado_int = int(''.join(individuo_mutado), 2)
    return individuo_mutado_int

def evoluir(selecionados, selecao_crossover, selecao_mutacao, probabilidade_mutacao_gerada, taxa_mutacao):
    """
    Realiza a evolução dos indivíduos selecionados.
    """
    filhos = []
    # Crossover
    selecao_crossover = [x - 1 for x in selecao_crossover]
    for i in range(0, len(selecao_crossover), 2):
        # Forma pares com os dois primeitos e dois ultimos indices de selecao_crossover 
        filhos.extend(crossover(selecionados[selecao_crossover[i]], selecionados[selecao_crossover[i+1]]))
    
    # Mutacao
    selecao_mutacao = [x - 1 for x in selecao_mutacao]
    for i in selecao_mutacao:
        filhos.append(mutacao(selecionados[i], probabilidade_mutacao_gerada, taxa_mutacao))

    return filhos

# Funcao principal
def main():
    dominio = [0, 128]
    tamanho_populacao = 4
    numeros_roleta_selecao = [12, 37, 78, 92]
    selecao_crossover = [1,3,2,4]
    selecao_mutacao = [1,3]
    probabilidade_mutacao_gerada = [12, 37, 78, 43, 2, 65, 98, 19, 4, 83, 7, 68]
    taxa_mutacao = 10
    # Gera a população inicial
    populacao = gerar_populacao(tamanho_populacao, dominio[0], dominio[1])
    print(f"Populacao inicial gerada: {populacao}")
    # Seleciona individuos da população paara evolução (crossover e/ou mutação)
    selecionados = selecao(populacao, numeros_roleta_selecao)
    print(f"Individuos selecionados para evolucao: {selecionados}")
    # Realiza a evolucao dos individuos selecionados
    filhos = evoluir(selecionados, selecao_crossover, selecao_mutacao, probabilidade_mutacao_gerada, taxa_mutacao)
    print(f"Nova população gerada: {filhos}")

if __name__ == "__main__":
    main()