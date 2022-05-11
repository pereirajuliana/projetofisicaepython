# Importação dos Módulos
import random
import sys
import pygame
from pygame.locals import *

# Definição de Parâmetros
LARGURA_TELA = 600
ALTURA_TELA = 499
QUADROS_POR_SEGUNDO = 32
GRAVIDADE = 1

janela = pygame.display.set_mode((LARGURA_TELA,ALTURA_TELA))
elevação = ALTURA_TELA*0.8
imagem_atual = 0
imagens_jogo = {}

IMAGEM_CANO = "imgs/pipe.png"
IMAGEM_FUNDO = "imgs/bg.png"
IMAGEM_SOLO = "imgs/base.png"
IMAGENS_PASSARO = ["imgs/bird1.png","imgs/bird2.png","imgs/bird3.png"]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 40)
FONTE_MSG = pygame.font.SysFont('arial', 20)
FONTE_FIM_DE_JOGO = pygame.font.SysFont('arial', 60)

def criarCano():
    deslocamento = ALTURA_TELA/3
    altura_cano = imagens_jogo["imagem_canos"][0].get_height()
    y2 = deslocamento + random.randrange(0,int(ALTURA_TELA - imagens_jogo["imagem_base"].get_height() - 1.2*deslocamento))
    canoX = LARGURA_TELA + 10
    y1 = altura_cano - y2 + deslocamento
    cano = [
        #cano superior
        {"x": canoX, "y":-y1},
        #cano inferior
        {"x": canoX, "y":y2}
        ]
    return cano

def fimJogo(horizontal, vertical, canos_superiores, canos_inferiores):
    if (vertical > elevação - 25 or vertical < 0):
        return True
    for cano in canos_superiores:
        altura_cano = imagens_jogo["imagem_canos"][0].get_height()
        if (vertical < altura_cano + cano["y"] and abs(horizontal - cano["x"]) < imagens_jogo["imagem_canos"][0].get_width()):
            return True
    for cano in canos_inferiores:
        if (vertical + imagens_jogo["imagens_pássaro"][0].get_height() > cano["y"]) and (abs(horizontal - cano["x"]) < imagens_jogo["imagem_canos"][0].get_width()):
            return True
        elif (vertical + imagens_jogo["imagens_pássaro"][1].get_height() > cano["y"]) and (abs(horizontal - cano["x"]) < imagens_jogo["imagem_canos"][0].get_width()):
            return True
        elif (vertical + imagens_jogo["imagens_pássaro"][2].get_height() > cano["y"]) and (abs(horizontal - cano["x"]) < imagens_jogo["imagem_canos"][0].get_width()):
            return True
    return False

def jogoFlappy():
    pontuação = 0
    horizontal = int(LARGURA_TELA/5)
    vertical = int(ALTURA_TELA/2)
    solo = 0
    altura_temp = 100
    
    # Gerando dois canos
    cano_1 = criarCano()
    cano_2 = criarCano()
    # Lista de canos inferiores
    canos_inferiores = [
        {"x":LARGURA_TELA+300-altura_temp,"y":cano_1[1]["y"]},
        {"x":LARGURA_TELA+300-altura_temp+(LARGURA_TELA/2),"y":cano_2[1]["y"]}
        ]
    # Lista de canos superiores
    canos_superiores = [
        {"x":LARGURA_TELA+300-altura_temp,"y":cano_1[0]["y"]},
        {"x":LARGURA_TELA+200-altura_temp+(LARGURA_TELA/2),"y":cano_2[0]["y"]}
        ]
    velocidade_cano_x = -4
    
    # Velocidade do pássaro
    vel_y_passaro = -9
    max_vel_y_passaro = 10
    min_vel_y_passaro = -8
    gravidade = GRAVIDADE
    
    vel_flap_passaro = -8
    passaro_agidado = False
    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT or (evento.type == KEYDOWN and evento.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN and (evento.key == K_SPACE or evento.key == K_UP):
                if (vertical > 0):
                    vel_y_passaro = vel_flap_passaro
                    passaro_agidado = True
        # se estiver travado
        fim_jogo = fimJogo(horizontal,vertical,canos_superiores,canos_inferiores)
        
        if fim_jogo:
            texto_fim_de_jogo = FONTE_FIM_DE_JOGO.render("Fim de Jogo!", 1, (0, 0, 0))
            print(texto_fim_de_jogo.get_width())
            janela.blit(texto_fim_de_jogo, (LARGURA_TELA/2 + 173 - texto_fim_de_jogo.get_width(), ALTURA_TELA/3))
            pygame.display.update()
            return
        
        # Verifica pontuação
        pos_jogador = horizontal + imagens_jogo["imagens_pássaro"][0].get_width()/2
        for cano in canos_superiores:
            cano_pos = cano["x"] + imagens_jogo["imagem_canos"][0].get_width()/2
            if cano_pos <= pos_jogador and pos_jogador < cano_pos + 4:
                pontuação += 1
                
        if vel_y_passaro < max_vel_y_passaro and not passaro_agidado:
            vel_y_passaro += gravidade
        
        if passaro_agidado:
            passaro_agidado = False
        
        altura_jogador = imagens_jogo["imagens_pássaro"][0].get_height()
        vertical += min(vel_y_passaro, elevação - vertical - altura_jogador)
        
        # movendo canos para esquerda
        for canoAlto, canoBaixo in zip(canos_superiores, canos_inferiores):
            canoAlto["x"] += velocidade_cano_x
            canoBaixo["x"] += velocidade_cano_x
        
        # Adicionar novo cano quando o primeiro está próximo do limite da tela à esquerda
        if 0 < canos_superiores[0]["x"] and canos_superiores[0]["x"] < 5:
            novoCano = criarCano()
            canos_superiores.append(novoCano[0])
            canos_inferiores.append(novoCano[1])
        
        # Remove canos fora da tela
        if canos_superiores[0]["x"] < -imagens_jogo["imagem_canos"][0].get_width():
            canos_superiores.pop(0)
            canos_inferiores.pop(0)
        
        # Limpando imagens do jogo
        janela.blit(imagens_jogo["imagem_fundo"],(0,0))
        for canoAlto, canoBaixo in zip(canos_superiores, canos_inferiores):
            janela.blit(imagens_jogo["imagem_canos"][0],(canoAlto["x"],canoAlto["y"]))
            janela.blit(imagens_jogo["imagem_canos"][1],(canoBaixo["x"],canoBaixo["y"]))
        
        janela.blit(imagens_jogo["imagem_base"], (solo,elevação))
        atualiza_passaro()
        janela.blit(imagens_jogo["imagens_pássaro"][imagem_atual],(horizontal,vertical))
        
        # buscando pontuação
        num = [int(x) for x in list(str(pontuação))]
        largura = 0
        
        for n in num:
            largura += imagens_jogo["imagens_pontos"][n].get_width()
        X_deslocamento = LARGURA_TELA/2 - 45
        
        texto = FONTE_PONTOS.render("Pontuação:", 1, (0, 0, 0))
        janela.blit(texto, (LARGURA_TELA/2 - 50 - texto.get_width(), 10))
        
        for n in num:
            janela.blit(imagens_jogo["imagens_pontos"][n], (X_deslocamento,ALTURA_TELA*0.03))
            X_deslocamento += imagens_jogo["imagens_pontos"][n].get_width()
        
        pygame.display.update()
        contador_quadros_por_segundo.tick(QUADROS_POR_SEGUNDO)

def atualiza_passaro():
    global imagem_atual
    imagem_atual = (imagem_atual + 1) % 3
    

# Começa o jogoFlappy()
if __name__ == "__main__":        
    pygame.init()
    contador_quadros_por_segundo = pygame.time.Clock()
    
    pygame.display.set_caption("Jogo - Flappy Bird")
    
    # Carrega as imagens do jogo
    imagens_jogo["imagens_pontos"] = (
        pygame.image.load("imgs/0.png").convert_alpha(),
        pygame.image.load("imgs/1.png").convert_alpha(),
        pygame.image.load("imgs/2.png").convert_alpha(),
        pygame.image.load("imgs/3.png").convert_alpha(),
        pygame.image.load("imgs/4.png").convert_alpha(),
        pygame.image.load("imgs/5.png").convert_alpha(),
        pygame.image.load("imgs/6.png").convert_alpha(),
        pygame.image.load("imgs/7.png").convert_alpha(),
        pygame.image.load("imgs/8.png").convert_alpha(),
        pygame.image.load("imgs/9.png").convert_alpha()
        )
    imagens_jogo["imagens_pássaro"] = (
        pygame.image.load(IMAGENS_PASSARO[0]).convert_alpha(),
        pygame.image.load(IMAGENS_PASSARO[1]).convert_alpha(),
        pygame.image.load(IMAGENS_PASSARO[2]).convert_alpha(),
        )
    imagens_jogo["imagem_base"] = pygame.transform.scale(pygame.image.load(IMAGEM_SOLO).convert_alpha(),(LARGURA_TELA,112))
    imagens_jogo["imagem_fundo"] = pygame.transform.scale(pygame.image.load(IMAGEM_FUNDO).convert_alpha(),(LARGURA_TELA,ALTURA_TELA))
    imagens_jogo["imagem_canos"] = (
        pygame.transform.rotate(pygame.image.load(IMAGEM_CANO).convert_alpha(), 180),
        pygame.image.load(IMAGEM_CANO).convert_alpha()
        )
    
    while True:
        horizontal = int(LARGURA_TELA/5)
        vertical = int((ALTURA_TELA - imagens_jogo["imagens_pássaro"][0].get_height())/2)
        solo = 0
        
        while True:
            for evento in pygame.event.get():
                if evento.type == QUIT or (evento.type == KEYDOWN and evento.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif evento.type == KEYDOWN and (evento.key == K_SPACE or evento.key == K_UP):
                    jogoFlappy()
                else:
                    janela.blit(imagens_jogo["imagem_fundo"],(0,0))
                    #atualiza_passaro()
                    janela.blit(imagens_jogo["imagens_pássaro"][imagem_atual],(horizontal,vertical))
                    janela.blit(imagens_jogo["imagem_base"], (solo,elevação))
                    
                    texto_boas_vindas = FONTE_MSG.render("Bem-vindo ao jogo Flappy Bird!!!", 1, (255, 255, 255))
                    janela.blit(texto_boas_vindas, ((LARGURA_TELA/2) + 145 - texto_boas_vindas.get_width(), ALTURA_TELA/3))
                    
                    texto_instruções = FONTE_MSG.render("Pressione Espaço ou Enter para iniciar o jogo.",1,(255,255,255))
                    janela.blit(texto_instruções, ((LARGURA_TELA/2) + 205.5 - texto_instruções.get_width(), ALTURA_TELA/3 + 40))
                    
                    pygame.display.update()
                    contador_quadros_por_segundo.tick(QUADROS_POR_SEGUNDO)
