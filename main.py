def mostra_tabuleiro(tabuleiro):
    print("-------------")
    for linha in tabuleiro:
        print("|", linha[0], "|", linha[1], "|", linha[2], "|")
        print("-------------")

def verifica_vitoria(tabuleiro, jogador):
    # Verifica sequência horizontal
    for i in range(0, 3):
        if tabuleiro[i][0] == jogador and tabuleiro[i][1] == jogador and tabuleiro[i][2] == jogador:
            return True

    # Verifica sequência vertical
    for i in range(0, 3):
        if tabuleiro[0][i] == jogador and tabuleiro[1][i] == jogador and tabuleiro[2][i] == jogador:
            return True

    # Verifica diagonal
    if tabuleiro[0][0] == jogador and tabuleiro[1][1] == jogador and tabuleiro[2][2] == jogador:
        return True
    if tabuleiro[0][2] == jogador and tabuleiro[1][1] == jogador and tabuleiro[2][0] == jogador:
        return True

    return False


def teste_terminal(estado):
    if verifica_vitoria(estado, 'X'):
        return 1
    if verifica_vitoria(estado, 'O'):
        return -1
    for linha in estado:
        for celula in linha:
            if celula == " ":
                return None
    return 0


def sucessores(estado, jogador_atual):
    lista_sucessores = []
    for i in range(3):
        for j in range(3):
            if estado[i][j] == " ":
                # Cria a cópia do tabuleiro nativamente, sem importar copy
                novo_estado = [linha[:] for linha in estado]
                novo_estado[i][j] = jogador_atual
                lista_sucessores.append(novo_estado)
    return lista_sucessores


def valor_max(estado):
    utilidade = teste_terminal(estado)
    if utilidade is not None:
        return utilidade

    v = -float('inf')

    for s in sucessores(estado, 'X'):
        v = max(v, valor_min(s))

    return v


def valor_min(estado):
    utilidade = teste_terminal(estado)
    if utilidade is not None:
        return utilidade

    v = float('inf')

    for s in sucessores(estado, 'O'):
        # Correção aplicada aqui: passa a vez para o valor_max!
        v = min(v, valor_max(s))

    return v


def decisao_minimax(estado):
    melhor_valor = -float('inf')
    melhor_jogada = None

    for s in sucessores(estado, 'X'):
        v = valor_min(s)
        if v > melhor_valor:
            melhor_valor = v
            melhor_jogada = s

    return melhor_jogada


def start_jogo():
    # Criação do tabuleiro vazio
    tabuleiro = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]

    print("=======================================")
    print("BEM-VINDO AO JOGO DA VELHA VS MINIMAX!")
    print("O Agente (IA) jogará como 'X'.")
    print("Você jogará como 'O'.")
    print("=======================================")

    # Define quem começa
    escolha = input("Quem começa? Digite 1 para o Agente(X) ou 2 para Você(O): ")
    jogador_atual = "X" if escolha == "1" else "O"

    mostra_tabuleiro(tabuleiro)

    # Loop principal do jogo
    while True:
        if jogador_atual == "O":
            # TURNO DO JOGADOR HUMANO
            print("Sua vez! (Você é o 'O')")
            while True:
                try:
                    linha = int(input("Escolha a linha (1 - 3): ")) - 1
                    coluna = int(input("Escolha a coluna (1 - 3): ")) - 1

                    if 0 <= linha <= 2 and 0 <= coluna <= 2 and tabuleiro[linha][coluna] == " ":
                        tabuleiro[linha][coluna] = "O"
                        break
                    else:
                        print("Posição inválida ou já ocupada. Tente novamente.")
                except ValueError:
                    print("Por favor, digite um número válido.")

        else:
            # TURNO DO AGENTE INTELIGENTE (X)
            print("\nVez do Agente (X). Pensando na melhor jogada...")
            tabuleiro = decisao_minimax(tabuleiro)

        mostra_tabuleiro(tabuleiro)

        # VERIFICA SE O JOGO ACABOU
        utilidade = teste_terminal(tabuleiro)

        if utilidade == 1:
            print("O Agente (X) venceu! O Minimax é implacável.")
            break
        elif utilidade == -1:
            print("Você venceu! (Se isso acontecer, tem algo errado na Matrix!)")
            break
        elif utilidade == 0:
            print("O jogo terminou empatado! Você sobreviveu à IA.")
            break

        # Altera o jogador para o próximo turno
        jogador_atual = "X" if jogador_atual == "O" else "O"


# Dê o start e divirta-se!
start_jogo()