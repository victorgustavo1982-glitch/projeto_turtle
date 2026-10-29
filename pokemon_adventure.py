import pygame
import random
import sys

pygame.init()

LARGURA, ALTURA = 900, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pokémon: Aventura")
RELOGIO = pygame.time.Clock()

FONTE = pygame.font.SysFont("arial", 22)
FONTE_GRANDE = pygame.font.SysFont("arial", 36, bold=True)
FONTE_PEQUENA = pygame.font.SysFont("arial", 17)

BRANCO = (245, 248, 255)
PRETO = (25, 30, 45)
VERDE = (74, 170, 100)
VERDE_ESCURO = (35, 115, 75)
AZUL = (72, 150, 230)
AMARELO = (255, 218, 75)
VERMELHO = (225, 75, 80)
CINZA = (220, 225, 235)
ROXO = (150, 100, 210)

POKEMON = {
    "Pikachu": {"tipo": "Elétrico", "cor": AMARELO, "hp": 42, "ataque": 12, "golpe": "Choque do Trovão"},
    "Charmander": {"tipo": "Fogo", "cor": (245, 125, 70), "hp": 46, "ataque": 13, "golpe": "Brasa"},
    "Bulbasaur": {"tipo": "Planta", "cor": (90, 180, 110), "hp": 50, "ataque": 10, "golpe": "Folha Navalha"},
    "Squirtle": {"tipo": "Água", "cor": (90, 165, 230), "hp": 48, "ataque": 11, "golpe": "Jato d'Água"},
}

def texto(msg, x, y, cor=PRETO, fonte=FONTE):
    imagem = fonte.render(msg, True, cor)
    TELA.blit(imagem, (x, y))

def desenhar_fundo():
    TELA.fill((145, 210, 245))
    pygame.draw.rect(TELA, (110, 195, 120), (0, 250, LARGURA, 350))
    pygame.draw.circle(TELA, (255, 230, 110), (790, 85), 42)
    # Nuvens
    for x, y in [(100, 75), (350, 110), (600, 55)]:
        pygame.draw.ellipse(TELA, BRANCO, (x, y, 75, 28))
        pygame.draw.ellipse(TELA, BRANCO, (x + 18, y - 12, 45, 35))
    # Caminho
    pygame.draw.polygon(TELA, (215, 190, 135), [(0, 390), (900, 330), (900, 470), (0, 540)])
    # Arbustos
    for x, y in [(80, 300), (180, 325), (720, 285), (820, 315)]:
        pygame.draw.circle(TELA, VERDE_ESCURO, (x, y), 27)
        pygame.draw.circle(TELA, VERDE, (x + 18, y - 8), 23)

def desenhar_pokemon(nome, x, y, escala=1.0, frente=False):
    info = POKEMON[nome]
    cor = info["cor"]
    r = int(42 * escala)
    # Sombra
    pygame.draw.ellipse(TELA, (75, 130, 80), (x-r, y+r, r*2, max(8, r//3)))
    # Corpo e cabeça em formas simples originais
    pygame.draw.ellipse(TELA, cor, (x-r, y-r, r*2, int(r*1.7)))
    pygame.draw.circle(TELA, cor, (x, y-r//2), int(r*0.82))
    # Orelhas estilizadas
    pygame.draw.polygon(TELA, cor, [(x-r//2, y-r), (x-r, y-r-int(r*.7)), (x-r//5, y-r//2)])
    pygame.draw.polygon(TELA, cor, [(x+r//2, y-r), (x+r, y-r-int(r*.7)), (x+r//5, y-r//2)])
    # Olhos
    pygame.draw.circle(TELA, PRETO, (x-r//3, y-r//2), max(3, r//8))
    pygame.draw.circle(TELA, PRETO, (x+r//3, y-r//2), max(3, r//8))
    pygame.draw.circle(TELA, BRANCO, (x-r//3+2, y-r//2-2), max(1, r//20))
    pygame.draw.circle(TELA, BRANCO, (x+r//3+2, y-r//2-2), max(1, r//20))
    # Bochechas
    pygame.draw.circle(TELA, (245, 95, 105), (x-r//2, y), max(3, r//7))
    pygame.draw.circle(TELA, (245, 95, 105), (x+r//2, y), max(3, r//7))
    pygame.draw.arc(TELA, PRETO, (x-r//4, y, r//2, r//3), 3.3, 6.1, max(2, int(2*escala)))

def botao(rect, rotulo, cor, mouse):
    cor_final = tuple(min(255, c + 18) for c in cor) if rect.collidepoint(mouse) else cor
    pygame.draw.rect(TELA, cor_final, rect, border_radius=12)
    pygame.draw.rect(TELA, BRANCO, rect, 2, border_radius=12)
    imagem = FONTE.render(rotulo, True, BRANCO)
    TELA.blit(imagem, imagem.get_rect(center=rect.center))

def barra_vida(x, y, vida, max_vida, largura=220):
    pygame.draw.rect(TELA, (80, 85, 95), (x, y, largura, 18), border_radius=7)
    preenchimento = max(0, int(largura * vida / max_vida))
    cor = (70, 200, 100) if vida > max_vida * .45 else (245, 175, 55) if vida > max_vida * .2 else VERMELHO
    pygame.draw.rect(TELA, cor, (x, y, preenchimento, 18), border_radius=7)
    pygame.draw.rect(TELA, BRANCO, (x, y, largura, 18), 2, border_radius=7)

def resetar_batalha():
    global inimigo, vida_inimigo, vida_jogador, mensagem, estado, capturas
    inimigo = random.choice([n for n in POKEMON if n != inicial])
    vida_inimigo = POKEMON[inimigo]["hp"]
    vida_jogador = POKEMON[inicial]["hp"]
    mensagem = f"Um {inimigo} selvagem apareceu!"
    estado = "batalha"
    capturas = 0

inicial = None
inimigo = None
vida_inimigo = 0
vida_jogador = 0
mensagem = "Escolha seu Pokémon inicial!"
estado = "escolha"
capturas = 0
vitorias = 0
pokebolas = 5
experiencia = 0
nivel = 1
botao_rects = {}
ultimo_golpe = ""

while True:
    mouse = pygame.mouse.get_pos()
    desenhar_fundo()
    clique = False

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            clique = True
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    if estado == "escolha":
        pygame.draw.rect(TELA, (255, 255, 255), (85, 45, 730, 495), border_radius=22)
        pygame.draw.rect(TELA, AZUL, (85, 45, 730, 495), 4, border_radius=22)
        texto("POKÉMON: AVENTURA", 260, 65, ROXO, FONTE_GRANDE)
        texto("Escolha seu parceiro inicial:", 300, 120)
        nomes = list(POKEMON.keys())
        botao_rects = {}
        posicoes = [(135, 190), (535, 190), (135, 355), (535, 355)]
        cores = [AMARELO, (245, 125, 70), (90, 180, 110), (90, 165, 230)]
        for i, nome in enumerate(nomes):
            x, y = posicoes[i]
            pygame.draw.rect(TELA, (240, 245, 252), (x, y, 230, 135), border_radius=15)
            desenhar_pokemon(nome, x+55, y+72, .55)
            texto(nome, x+105, y+25, PRETO)
            texto(POKEMON[nome]["tipo"], x+105, y+55, ROXO, FONTE_PEQUENA)
            texto(f"HP {POKEMON[nome]['hp']}  ATQ {POKEMON[nome]['ataque']}", x+105, y+80, PRETO, FONTE_PEQUENA)
            botao_rects[nome] = pygame.Rect(x, y, 230, 135)
        texto("Clique em um Pokémon para começar", 270, 500, VERDE_ESCURO, FONTE_PEQUENA)
        if clique:
            for nome, rect in botao_rects.items():
                if rect.collidepoint(mouse):
                    inicial = nome
                    resetar_batalha()
                    estado = "batalha"

    elif estado == "batalha":
        pygame.draw.rect(TELA, (255, 255, 255), (30, 25, 840, 535), border_radius=20)
        pygame.draw.rect(TELA, AZUL, (30, 25, 840, 535), 4, border_radius=20)
        texto("ROTA 1  •  BATALHA", 55, 42, ROXO, FONTE_GRANDE)
        # Painel do inimigo
        pygame.draw.rect(TELA, (235, 245, 255), (470, 100, 340, 125), border_radius=15)
        texto(f"{inimigo} selvagem", 495, 115)
        texto(f"HP {vida_inimigo}/{POKEMON[inimigo]['hp']}", 495, 148, PRETO, FONTE_PEQUENA)
        barra_vida(495, 175, vida_inimigo, POKEMON[inimigo]["hp"], 260)
        desenhar_pokemon(inimigo, 650, 280, .9)
        # Painel do jogador
        pygame.draw.rect(TELA, (235, 250, 235), (55, 285, 340, 125), border_radius=15)
        texto(f"{inicial} (Nv. {nivel})", 80, 300)
        texto(f"HP {vida_jogador}/{POKEMON[inicial]['hp']}", 80, 333, PRETO, FONTE_PEQUENA)
        barra_vida(80, 358, vida_jogador, POKEMON[inicial]["hp"], 260)
        desenhar_pokemon(inicial, 270, 235, .9)
        # Caixa de mensagem
        pygame.draw.rect(TELA, (248, 249, 255), (55, 420, 790, 58), border_radius=10)
        pygame.draw.rect(TELA, (160, 170, 195), (55, 420, 790, 58), 2, border_radius=10)
        texto(mensagem[:75], 75, 438, PRETO, FONTE_PEQUENA)
        # Botões
        botao_rects = {
            "atacar": pygame.Rect(60, 490, 175, 48),
            "capturar": pygame.Rect(250, 490, 175, 48),
            "curar": pygame.Rect(440, 490, 175, 48),
            "fugir": pygame.Rect(630, 490, 175, 48),
        }
        botao(botao_rects["atacar"], "ATACAR", VERMELHO, mouse)
        botao(botao_rects["capturar"], f"POKÉBOLA ({pokebolas})", AZUL, mouse)
        botao(botao_rects["curar"], "POÇÃO", VERDE, mouse)
        botao(botao_rects["fugir"], "PRÓXIMO", ROXO, mouse)

        if clique:
            if botao_rects["atacar"].collidepoint(mouse):
                dano = random.randint(max(4, POKEMON[inicial]["ataque"] - 3), POKEMON[inicial]["ataque"] + 4)
                vida_inimigo = max(0, vida_inimigo - dano)
                mensagem = f"{inicial} usou {POKEMON[inicial]['golpe']}! Dano: {dano}."
                if vida_inimigo <= 0:
                    experiencia += 20
                    vitorias += 1
                    if experiencia >= nivel * 30:
                        experiencia = 0
                        nivel += 1
                        mensagem = f"Vitória! {inicial} subiu para o nível {nivel}!"
                    else:
                        mensagem = f"Você venceu! +20 XP. Vitórias: {vitorias}."
                    estado = "vitoria"
                else:
                    dano_inimigo = random.randint(5, 12)
                    vida_jogador = max(0, vida_jogador - dano_inimigo)
                    mensagem += f" O inimigo atacou: -{dano_inimigo} HP."
                    if vida_jogador <= 0:
                        estado = "derrota"
                        mensagem = "Seu Pokémon ficou sem HP! Tente novamente."
            elif botao_rects["capturar"].collidepoint(mouse):
                if pokebolas <= 0:
                    mensagem = "Você não tem mais Pokébolas!"
                elif vida_inimigo > POKEMON[inimigo]["hp"] * .55:
                    pokebolas -= 1
                    mensagem = "Está com muita energia! Tente enfraquecer antes."
                else:
                    pokebolas -= 1
                    if random.random() < .65:
                        capturas += 1
                        mensagem = f"{inimigo} foi capturado! Capturas: {capturas}."
                        estado = "captura"
                    else:
                        mensagem = "Oh, escapou da Pokébola! Tente de novo."
            elif botao_rects["curar"].collidepoint(mouse):
                vida_jogador = min(POKEMON[inicial]["hp"], vida_jogador + 18)
                mensagem = "Você usou uma poção e recuperou até 18 HP!"
            elif botao_rects["fugir"].collidepoint(mouse):
                resetar_batalha()

    elif estado in ("vitoria", "captura", "derrota"):
        pygame.draw.rect(TELA, (255, 255, 255), (100, 70, 700, 460), border_radius=25)
        pygame.draw.rect(TELA, AZUL, (100, 70, 700, 460), 4, border_radius=25)
        if estado == "vitoria":
            texto("VITÓRIA!", 340, 100, VERDE_ESCURO, FONTE_GRANDE)
            desenhar_pokemon(inicial, 450, 240, 1.15)
            texto(f"{inicial} ganhou experiência!", 285, 320)
        elif estado == "captura":
            texto("POKÉMON CAPTURADO!", 240, 100, ROXO, FONTE_GRANDE)
            desenhar_pokemon(inimigo, 450, 240, 1.15)
            texto(f"{inimigo} entrou para sua coleção!", 275, 320)
        else:
            texto("FIM DE BATALHA", 300, 100, VERMELHO, FONTE_GRANDE)
            desenhar_pokemon(inicial, 450, 240, 1.15)
            texto("Seu parceiro precisa descansar.", 280, 320)
        texto(f"Vitórias: {vitorias}   Capturas: {capturas}   Pokébolas: {pokebolas}", 225, 370, PRETO, FONTE_PEQUENA)
        botao_rects = {"continuar": pygame.Rect(300, 420, 300, 55)}
        botao(botao_rects["continuar"], "CONTINUAR AVENTURA", VERDE_ESCURO, mouse)
        if clique and botao_rects["continuar"].collidepoint(mouse):
            if estado == "derrota":
                vida_jogador = POKEMON[inicial]["hp"]
            resetar_batalha()

    pygame.display.flip()
    RELOGIO.tick(60)
