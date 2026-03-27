def mostra_tabuleiro(tabuleiro):
    print("-------------")
    for linha in tabuleiro:
        print("|", linha[0], "|", linha[1], "|", linha[2], "|")
        print("-------------")

def verifica_vitoria(tabuleiro, jogador):
    # sequência horizontal
    for i in range(0, 3):
        if tabuleiro[i][0] == jogador and tabuleiro[i][1] == jogador and tabuleiro[i][2] == jogador:
            return True

    # sequência vertical
    for i in range(0, 3):
        if tabuleiro[0][i] == jogador and tabuleiro[1][i] == jogador and tabuleiro[2][i] == jogador:
            return True

    # diagonal
    if tabuleiro[0][0] == jogador and tabuleiro[1][1] == jogador and tabuleiro[2][2] == jogador:
        return True
    if tabuleiro[0][2] == jogador and tabuleiro[1][1] == jogador and tabuleiro[2][0] == jogador:
        return True

    return False

def teste_terminal(estado,jogador,adversario):
    # agente ganhou
    if verifica_vitoria(estado, adversario):
        return 1
    # humano ganhou
    if verifica_vitoria(estado, jogador):
        return -1
    # jogo não terminou
    for linha in estado:
        for celula in linha:
            if celula == " ":
                return None
    #empate
    return 0

# cria todas as jogadas possíveis
def sucessores(estado, jogador_atual):
    lista_sucessores = []
    for i in range(3):
        for j in range(3):
            if estado[i][j] == " ":
                # cópia do tabuleiro
                novo_estado = [linha[:] for linha in estado]
                novo_estado[i][j] = jogador_atual
                lista_sucessores.append(novo_estado)
    return lista_sucessores

def valor_max(estado, jogador, agente):
    # verifica se o jogo acabou
    utilidade = teste_terminal(estado, jogador, agente)
    if utilidade is not None:
        return utilidade
    
    # pior valor possível
    v = -float('inf')
    
    # testa todas as jogadas possíveis
    for s in sucessores(estado, agente):
        # melhor resultado
        v = max(v, valor_min(s, jogador, agente))
        
    return v

def valor_min(estado, jogador, agente):
    # verifica se o jogo acabou
    utilidade = teste_terminal(estado, jogador, agente)
    if utilidade is not None:
        return utilidade
    v = float('inf')
    

    for s in sucessores(estado, jogador):
        # jogada que mais atrapalha o humano
        v = min(v, valor_max(s, jogador, agente))
    return v

# escolhe a jogada
def decisao_minimax(estado, jogador, agente):
    melhor_valor = -float('inf')
    melhor_jogada = None
    
    for s in sucessores(estado, agente):
        v = valor_min(s, jogador, agente)
        if v > melhor_valor:
            melhor_valor = v
            melhor_jogada = s
            
    return melhor_jogada


def start_jogo():
    tabuleiro = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    
    escolha = ""
    while escolha != "1" and escolha != "2":
        escolha = input("Digite 1 para jogar como X ou 2 para O: ")

    if escolha == "1":
        jogador = "X"
        adversario = "O"
    else:
        jogador = "O"
        adversario = "X"
    

    jogador_atual = "X"
    mostra_tabuleiro(tabuleiro)

    # loop principal do jogo
    while True:
        if jogador_atual == jogador:
            # vez da pessoa
            print(f"\nSua vez! (Você é o '{jogador}')")
            while True:
                try:
                    linha = int(input("Escolha a linha (1 - 3): ")) - 1
                    coluna = int(input("Escolha a coluna (1 - 3): ")) - 1
                    if 0 <= linha <= 2 and 0 <= coluna <= 2 and tabuleiro[linha][coluna] == " ":
                        tabuleiro[linha][coluna] = jogador
                        break
                    else:
                        print("Posição inválida ou ocupada.")
                except ValueError:
                    print("Digite números de 1 a 3.")
        else:
            # vez do agente
            print(f"\nVez do Agente ({adversario}).")
 
            tabuleiro = decisao_minimax(tabuleiro, jogador, adversario)

        mostra_tabuleiro(tabuleiro)

        # verificação de fim de jogo
        utilidade = teste_terminal(tabuleiro, jogador, adversario)
        
        if utilidade is not None: 
            if utilidade == 1:
                print(f"O Agente ({adversario}) venceu!")
            elif utilidade == -1:
                print("Você venceu!")
            else:
                print("Empate!")
            break

        # próximo turno
        jogador_atual = "O" if jogador_atual == "X" else "X"

start_jogo()