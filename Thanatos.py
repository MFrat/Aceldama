__author__ = 'Max'

from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.collision import *
from PPlay.mouse import *
from PPlay.gameobject import *
from PPlay.sound import *
import pygame
import random
import time

def criar_janela(x, y):
    janela = Window(x, y)
    janela.set_title('Thanatos')
    return janela

def menu_inicial(x, y):
    fundo_menu = GameImage('sprites/menuInicial.png')
    botao_play = Sprite('sprites/playMenu.png')
    botao_ranking = Sprite('sprites/rankingMenu.png')
    botao_instrucoes = Sprite('sprites/instrucoesMenu.png')
    botao_sair = Sprite('sprites/sairMenu.png')

    fundo_menu.draw()
    botao_play.set_position(0, y/30 + botao_play.height/2)
    botao_play.draw()
    botao_ranking.set_position(0, y/30 + botao_ranking.height/2 + 50)
    botao_ranking.draw()
    botao_instrucoes.set_position(0, y/30 + botao_instrucoes.height/2 + 120)
    botao_instrucoes.draw()
    botao_sair.set_position(0, y/30 + botao_sair.height/2 + 180)
    botao_sair.draw()

    if(mouse.is_over_object(botao_play) and mouse.is_button_pressed(1)):
        return 1
    elif (mouse.is_over_object(botao_ranking) and mouse.is_button_pressed(1)):
        return 3
    elif (mouse.is_over_object(botao_instrucoes) and mouse.is_button_pressed(1)):
        return 1.2
    elif (mouse.is_over_object(botao_sair) and mouse.is_button_pressed(1)):
        return 4
    else:
        return 0

def scrolling(): #Efetua o Scrolling da plano de fundo.
    fundo_city.move_y(fundo_city.speed * Janela.delta_time())
    fundo_city2.move_y(fundo_city.speed * Janela.delta_time())

    if round(fundo_city.y, 0) >= 600:
        fundo_city.set_position(0, -3500)
    elif round(fundo_city2.y, 0) >= 600:
        fundo_city2.set_position(0, -3500)

    fundo_city.draw()
    fundo_city2.draw()

def movimentação_jogador():
    if jogador.x < 110:
        jogador.x = 110
    elif jogador.x + jogador.width >= 690:
        jogador.x = 690 - jogador.width

    jogador.move_key_x(jogador.velocidade * Janela.delta_time())
    jogador.draw()

def pontuação():
    jogador.pontos += 1
    jogador.pontos_aux += 1
    jogador.pontos_aux_nitro += 1

def jogador_vida(situação):
    if jogador.vida <= 100:
        jogador.vida += 5*situação
    elif jogador.vida > 100:
        jogador.vida = 100

def aumenta_gasolina():
    if jogador.gasolina < 100:
        jogador.gasolina += 10

def controle_munição(situação):
    jogador.ammo += 1 * situação

def jogador_gasolina():
    if gasolina.tempo >= decremento_gasolina:
        jogador.gasolina -= 5
        gasolina.tempo = 0
    else:
        gasolina.tempo = gasolina.tempo

def spawn_and_collision():
    for spr in vetor_posições_sprites:
        if spr.id == 'zumbi':
            spr.move_y((fundo_city.speed + 50) * Janela.delta_time())
        else:
            spr.move_y(fundo_city.speed * Janela.delta_time())

        if spr.y >= 600:
            x = random.randint(200,600)
            spr.set_position(x,-200)

        spr.set_total_duration(250)
        spr.update()

        if(spr.collided(jogador)):
            if(spr.id == "zumbi" or spr.id == "barricada" or spr.id == "barricada_madeira" or spr.id == "healer" or spr.id == 'ammobox'):
                if(spr.id == "zumbi" ):
                    pontuação()
                    atropelamento.play()
                elif spr.id == 'ammobox':
                    controle_munição(spr.sit)
                jogador_vida(spr.sit)
                x = random.randint(200, 600)
                spr.set_position(x, -200)

        spr.draw()




    if Collision.collided(barricada, tiro):
            tiro.set_position(1000,1000)


    if Collision.collided(barricada_madeira, tiro):
        x = random.randint(200,600)
        tiro.set_position(1000,1000)
        barricada_madeira.set_position(x,-200)
        barricada_madeira.draw()

    if Collision.collided(tiro, zumbi):
        x = random.randint(200,600)
        pontuação()
        zumbi.set_position(x,-200)
        tiro.set_position(1000,1000)
        zumbi.draw()

    if Collision.collided(gasolina, jogador):
        x = random.randint(200,600)
        aumenta_gasolina()
        gasolina.set_position(x,-200)
        gasolina.draw()

def verifica_fim():
    if jogador.vida <= 0:
        return 2
    if jogador.gasolina <= 0:
        return 2
    else:
        return 1

def reset_status():
    jogador.vida = 100
    jogador.gasolina = 100
    jogador.pontos = 0
    jogador.ammo = 10
    jogador.nitro = 0
    noite1.tempo = 0

def tela_derrota():
    fundo_perdeu.draw()
    botao_sair_final = Sprite('sprites/sair_final.png')
    botao_jogar_novamente = Sprite('sprites/jogar_novamente.png')
    botao_ranking = Sprite('sprites/ranking_final.png')
    botao_jogar_novamente.set_position(250, 300)
    botao_sair_final.set_position(255 + botao_jogar_novamente.width, 300)
    botao_ranking.set_position(255, 500)
    botao_jogar_novamente.draw()
    botao_sair_final.draw()
    botao_ranking.draw()
    Janela.draw_text('Você fez: ' + str(jogador.pontos) + ' pontos.', 0, 25, 25, (255,255,255), "Calibri", True)

    if jogador.gasolina <= 0:
        Janela.draw_text('Você ficou sem gasolina.', 0, 50, 25, (255,255,255), "Calibri", True)
    elif jogador.vida <= 0:
        Janela.draw_text('Voce bateu demais =/.', 0, 75, 25, (255,255,255), "Calibri", True)

    if (mouse.is_over_object(botao_jogar_novamente) and mouse.is_button_pressed(1)):
        reset_status()
        return 1
    elif (mouse.is_over_object(botao_sair_final) and mouse.is_button_pressed(1)):
        return 4
    elif (mouse.is_over_object(botao_ranking) and mouse.is_button_pressed(1)):
        return 3

    return 2

def killStreak_stunts(som):
    dicionario_sons = {'Combo_whore': combo_whore_sprite, 'Double_kill': double_kill_sprite, 'Dominating': dominating_sprite,
                       'Ownage': ownage_sprite, 'Godlike': godlike_sprite, 'Holyshit': holy_shit_sprite, 'Mega_kill': mega_kill_sprite,
                       'Monster_kill': monster_kill_sprite, 'First_blood': first_blood_sprite}

    if som != '' and fundo_city.tempo_animação > 0:
        dicionario_sons[som].move_key_y(-fundo_city.speed)
        dicionario_sons[som].draw()
        fundo_city.tempo_animação -= Janela.delta_time()

    if fundo_city.tempo_animação <= 0:
            jogador.killStreak = ''
            fundo_city.tempo_animação = 3

def sons(vetor):
    sons2 = [Dominating, Ownage, Godlike, Holyshit]
    sons3 = [Mega_kill, Monster_kill, Combo_whore, Double_kill]
    sons2_aux = ['Dominating', 'Ownage', 'Godlike', 'Holyshit']
    sons3_aux = ['Mega_kill', 'Monster_kill', 'Combo_whore', 'Double_kill']
    vetor_aux = []

    if jogador.tempo >= tempo_reset_vetor:
        jogador.tempo = 0
        vetor_aux = ['1']
        return vetor_aux

    if jogador.pontos_aux == 1 and '1' not in vetor:
        First_blood.play()
        jogador.killStreak = 'First_blood'
        fundo_city.tempo_animação = 3
        vetor += ['1']

    elif jogador.pontos_aux == 3 and '2' not in vetor:
        aleatorio = random.randint(0,3)
        jogador.killStreak = sons2_aux[aleatorio]
        fundo_city.tempo_animação = 3
        sons2[aleatorio].play()
        vetor += ['2']

    elif jogador.pontos_aux == 5 and '3' not in vetor:
        aleatorio = random.randint(0,3)
        jogador.killStreak = sons3_aux[aleatorio]
        fundo_city.tempo_animação = 3
        sons3[aleatorio].play()
        vetor += ['3']
        jogador.pontos_aux = 0
        vetor_aux = ['1']
        return vetor_aux

    return vetor

def tiro_jogador():
    tiro.move_y(-tiro.velocidade * Janela.delta_time())
    tiro.draw()
    tiro.update()

    if jogador.tempo_tiro >= 1 and (keyboard.key_pressed("space")) and jogador.ammo > 0:
        Tiro_sound.play()
        controle_munição(-1)
        tiro.set_position(jogador.x, jogador.y)
        jogador.tempo_tiro = 0
    else:
        jogador.tempo_tiro = jogador.tempo_tiro

def hub_jogador():
    hub_background.set_position(0,0)
    hub_background.draw()
    Janela.draw_text('Pontuação: ' + str(jogador.pontos), 0, 0, 20, (255,255,255), "Calibri", True)
    Janela.draw_text('Vida: ' + str(jogador.vida) + '%', 0, 25, 20, (255,255,255), "Calibri", True)
    Janela.draw_text('Gasolina: ' + str(jogador.gasolina), 0, 50, 20, (255,255,255), "Calibri", True)
    Janela.draw_text('Munição: ' + str(jogador.ammo), 0, 75, 20, (255,255,255), "Calibri", True)
    Janela.draw_text('Nitro: ' + jogador.nitro_ready, 0, 100, 20, (255,0,0), "Calibri", True)


    if jogador.nitro_ready == 'Ready':
        Janela.draw_text('Nitro: ' + jogador.nitro_ready, 0, 100, 20, (0,255,0), "Calibri", True)

    if jogador.vida < 20:
        Janela.draw_text('Vida: ' + str(jogador.vida) + '%', 0, 25, 20, (255,0,0), "Calibri", True)

    if jogador.ammo < 3:
        Janela.draw_text('Munição: ' + str(jogador.ammo), 0, 75, 20, (255,0,0), "Calibri", True)

    if jogador.gasolina < 20:
        Janela.draw_text('Gasolina: ' + str(jogador.gasolina), 0, 50, 20, (255,0,0), "Calibri", True)

def verifica_pause():
    if keyboard.key_pressed('enter') and GameState == 1.1:
        return 1
    elif keyboard.key_pressed('esc'):
        return 1.1
    else:
        return GameState

def tela_pause():
    for sprite in vetor_sprites_pause:
        sprite.draw()

    Janela.draw_text('Paused.', round(x/2 - 20), round(y/2 - 20), 20, (255,255,255), "Calibri", True)
    anoitecer()
    hub_jogador()

def nitro():
    if jogador.pontos_aux_nitro >= 4:
        jogador.nitro_ready = 'Ready'
    else:
        jogador.nitro_ready = 'Empty'

    if keyboard.key_pressed('LEFT_SHIFT') and jogador.pontos_aux_nitro >= 4:
        fundo_city.speed = 500
        jogador.nitro_sit = 'on'

    if jogador.nitro_sit == 'on':
        jogador.nitro -= Janela.delta_time()

    if jogador.nitro <= 0:
        jogador.nitro_sit = 'off'
        jogador.pontos_aux_nitro = 0
        fundo_city.speed = 300
        jogador.nitro = 3

def controle_tempo():
    gasolina.tempo += Janela.delta_time()
    jogador.tempo += Janela.delta_time()
    jogador.tempo_tiro += Janela.delta_time()
    noite1.tempo += Janela.delta_time()

def anoitecer():
    if noite1.tempo >= 40 and noite1.tempo < 120:
        noite1.draw()
    elif noite1.tempo >= 120 and noite1.tempo < 180:
        noite2.draw()
    elif noite1.tempo >= 180:
        noite3.draw()

def pergunta_nome():
    if jogador.nome_sit == 0:
        while True:
            jogador.nome = input('Digite seu nome: ')
            if ' ' in jogador.nome:
                print('Sem espaços.')
            else:
                break

    jogador.nome_sit = 1

def leArquivo_ranking():
    arquivo_ranking = open('ranking.txt', 'r')
    vetor_nomes = []
    vetor_pontos = []
    linhas_arquivo = []

    linhas_arquivo_aux = arquivo_ranking.readlines()

    for i in linhas_arquivo_aux:
        string_aux = i.strip()
        linhas_arquivo += [string_aux.split()]

    for i in range(len(linhas_arquivo)):
        vetor_nomes += [linhas_arquivo[i][0]]
        vetor_pontos += [linhas_arquivo[i][1]]

    return vetor_nomes, vetor_pontos

def novoNome_ranking(vetor_nomes, vetor_pontos):
    arquivo_ranking = open('ranking.txt', 'a')

    if jogador.nome not in vetor_nomes:
        arquivo_ranking.write('\n' + jogador.nome + ' ' + str(jogador.pontos))
        vetor_nomes += [jogador.nome]
        vetor_pontos += [jogador.pontos]

    arquivo_ranking.close()

    return vetor_nomes, vetor_pontos

def escreveArquivo_ranking(vetor_nomes, vetor_pontos):
    arquivo_ranking = open('ranking.txt', 'w')

    if jogador.nome in vetor_nomes:
        posição = vetor_nomes.index(jogador.nome)
        vetor_pontos[posição] = jogador.pontos

    for i in range(len(vetor_pontos)):
        for j in range(i, len(vetor_pontos)):
            if int(vetor_pontos[i]) < int(vetor_pontos[j]):
                aux = vetor_pontos[i]
                vetor_pontos[i] = vetor_pontos[j]
                vetor_pontos[j] = aux

                aux2 = vetor_nomes[i]
                vetor_nomes[i] = vetor_nomes[j]
                vetor_nomes[j] = aux2

    for i in range(len(vetor_pontos)):
        arquivo_ranking.write((vetor_nomes[i] + ' ' + str(vetor_pontos[i]) + '\n'))

    arquivo_ranking.close()

def escreveTela_ranking():
    arquivo_ranking = open('ranking.txt', 'r')
    vetor_nomes = []
    vetor_pontos = []
    linhas_arquivo = []
    fundo_voltar = Sprite('sprites/Voltar.png')
    fundo_voltar.set_position(x-fundo_voltar.width,y-fundo_voltar.height)
    fundo_voltar.draw()

    linhas_arquivo_aux = arquivo_ranking.readlines()

    for i in linhas_arquivo_aux:
        string_aux = i.strip()
        linhas_arquivo += [string_aux.split()]

    for i in range(len(linhas_arquivo)):
        vetor_nomes += [linhas_arquivo[i][0]]
        vetor_pontos += [linhas_arquivo[i][1]]

    for i in range(len(vetor_pontos)):
        for j in range(i, len(vetor_pontos)):
            if int(vetor_pontos[i]) < int(vetor_pontos[j]):
                aux = vetor_pontos[i]
                vetor_pontos[i] = vetor_pontos[j]
                vetor_pontos[j] = aux

                aux2 = vetor_nomes[i]
                vetor_nomes[i] = vetor_nomes[j]
                vetor_nomes[j] = aux2

    for i in range(len(vetor_pontos)):
        Janela.draw_text(str(i+1) + ': ' + str(vetor_nomes[i]) + ' ' + str(vetor_pontos[i]), (x/2)-40, (i*25)+100, 20, (255,255,255), "Calibri", True)

    if(mouse.is_over_object(fundo_voltar) and mouse.is_button_pressed(1)):
        return 0
    else:
        return 3

def tela_instrocao():
    fundo_instrucao.draw()
    fundo_instrucao_voltar.set_position(x-fundo_instrucao_voltar.width,y-fundo_instrucao_voltar.height)
    fundo_instrucao_voltar.draw()

    if(mouse.is_over_object(fundo_instrucao_voltar) and mouse.is_button_pressed(1)):
        return 0
    else:
        return 1.2

#resolução
x = 800
y = 600

#cria janela e usa a função get.mouse() e get_keyboard().
Janela = criar_janela(x,y)
mouse = criar_janela(x, y).get_mouse()
keyboard = Janela.get_keyboard()

#define os sprites.
fundo_city = Sprite('sprites/Game_Loop_Fundo.png')
fundo_instrucao = Sprite('sprites/Instrucoes.png')
fundo_instrucao_voltar = Sprite('sprites/Voltar.png')
zumbi = Sprite('sprites/Zombie.png', 4)
fundo_city2 = Sprite('sprites/Game_Loop_Fundo.png')
jogador = Sprite('sprites/Veiculo.png')
barricada = Sprite('sprites/barricada.png')
healer = Sprite('sprites/healer.png', 2)
fundo_perdeu = Sprite('sprites/perdeu_fundo.png')
gasolina = Sprite('sprites/gasolina.png', 2)
tiro = Sprite('sprites/tiro.png', 8)
tiro.set_total_duration(200)
barricada_madeira = Sprite('sprites/barricada_madeira.png')
ammobox = Sprite('sprites/ammo.png', 2)
bandit_tiro = Sprite('sprites/tiro.png')
bandit = Sprite('sprites/Zombie.png')
hub_background = Sprite('sprites/hub_background.png')
noite1 = Sprite('sprites/Noite33%.png')
noite2 = Sprite('sprites/Noite66%.png')
noite3 = Sprite('sprites/Noite80%.png')
fundo_ranking = Sprite('sprites/fundo_ranking.png')

#stunts dos kills streaks do jogador.
fundo_city.tempo_animação = 3
jogador.killStreak = ''
combo_whore_sprite = Sprite('sprites/Combo_whore_sprite.png')
double_kill_sprite = Sprite('sprites/Double_kill_sprite.png')
dominating_sprite = Sprite('sprites/Dominating_sprite.png')
ownage_sprite = Sprite('sprites/Ownage_sprite.png')
godlike_sprite = Sprite('sprites/Godlike_sprite.png')
holy_shit_sprite = Sprite('sprites/Holyshit_sprite.png')
mega_kill_sprite = Sprite('sprites/Megakill_sprite.png')
monster_kill_sprite = Sprite('sprites/Monsterkill_sprite.png')
first_blood_sprite = Sprite('sprites/First_blood_sprite.png')

vetor_sprites_stunts = [combo_whore_sprite, double_kill_sprite, dominating_sprite, ownage_sprite, godlike_sprite,
                        holy_shit_sprite, mega_kill_sprite, monster_kill_sprite, first_blood_sprite]

for i in vetor_sprites_stunts:
    i.set_position(x/2 - (i.width/2), 10)

#anoitecer
noite1.tempo = 0

#alguns elementos dos sprites.
jogador.id = 'jogador'
barricada_madeira.id = "barricada_madeira"
barricada_madeira.sit = -1.8
gasolina.id = "gasolina"
gasolina.sit = 1
healer.id = "healer"
healer.sit = 1
barricada.id = "barricada"
barricada.sit = -2
zumbi.id = "zumbi"
zumbi.sit = -1.5
ammobox.id = "ammobox"
ammobox.sit = 1

#define as posições inciais de cada sprite.
vetor_posições_sprites = [zumbi, barricada, healer, gasolina, barricada_madeira, ammobox]
vetor_sprites_pause = [fundo_city, fundo_city2, zumbi, barricada, healer, gasolina, barricada_madeira, ammobox, jogador, tiro]
fundo_city2.set_position(0,-3500)
jogador.set_position(x/2 - jogador.width/2, y - jogador.height)

for sprite in vetor_posições_sprites:
    x1 = random.randint(100, 400)
    y1 = random.randint(50, 2000)
    sprite.set_position(x1, -y1)

#velocidade de movimento do scrolling do plano de fundo.
jogador.velocidade = 200
fundo_city.speed = 300

#O GameState controla o fluxo do jogo.
GameState = 0

#sons.
Godlike = Sound('audio/Godlike.ogg')
First_blood = Sound('audio/First_blood.ogg')
Holyshit = Sound('audio/Holyshit.ogg')
Dominating = Sound('audio/Dominating.ogg')
Killing_spree = Sound('audio/Killing_spree.ogg')
Monster_kill = Sound('audio/Monster_kill.ogg')
Mega_kill = Sound('audio/Mega_kill.ogg')
Ownage = Sound('audio/Ownage.ogg')
atropelamento = Sound('audio/atropelando.ogg')
Combo_whore = Sound('audio/Combo_whore.ogg')
Double_kill = Sound('audio/Double_kill.ogg')
Tiro_sound = Sound('audio/tiro_sound.ogg')
vetor_sons = [] #Auxilia na emissão dos sons.
jogador.pontos_aux = 0 #Auxilia na emissão dos sons.

#nitro
jogador.nitro_sit = 'off'
jogador.nitro = 3
jogador.nitro_ready = 'Empty'
jogador.pontos_aux_nitro = 0 #Auxilia na contagem do nitro.

#dados da HUB do jogador.
jogador.pontos = 0
jogador.vida = 100
jogador.gasolina = 100
jogador.ammo = 10
decremento_gasolina = 1.5
tiro.velocidade = 1000
jogador.nome = ' '

#tempo
gasolina.tempo = 3
tempo_delay_tiro = 1
jogador.tempo = 0 #auxilia no reset do vetor dos sons.
jogador.tempo_tiro = 0
tempo_reset_vetor = 30 #Tempo para resetar o vetor de sons.

#Auxiliares para o ranqueamento.
jogador.nome_sit = 0
vetor_nomes = []
vetor_pontos = []

#main
while True:
    #GameState1 = Menu de jogo.
    if GameState == 0:
        GameState = menu_inicial(x, y)

    #GameState2 = Loop principal do jogo.
    elif GameState == 1:
        jogador.nome_sit = 0
        GameState = verifica_fim()
        controle_tempo()
        scrolling()
        spawn_and_collision()
        movimentação_jogador()
        anoitecer()
        tiro_jogador()
        nitro()
        jogador_gasolina()
        vetor_sons = sons(vetor_sons)
        hub_jogador()
        GameState = verifica_pause()
        killStreak_stunts(jogador.killStreak)

    #GameState1.1 = pause.
    elif GameState == 1.1:
        GameState = verifica_pause()
        tela_pause()

    #GameState1.2 = instruções do jogo.
    elif GameState == 1.2:
        GameState = tela_instrocao()

    #GameState2 = tela derrota.
    elif GameState == 2:
        pergunta_nome()
        vetor_nomes, vetor_pontos = leArquivo_ranking()
        vetor_nomes, vetor_pontos = novoNome_ranking(vetor_nomes, vetor_pontos)
        escreveArquivo_ranking(vetor_nomes, vetor_pontos)
        GameState = tela_derrota()

    #GameState3 = Tela de Ranking.
    elif GameState == 3:
        reset_status()
        fundo_ranking.draw()
        GameState = escreveTela_ranking()

    #GameState3 = sair do jogo.
    elif GameState == 4:
        break

    Janela.update()