import M5
from M5 import *
from hardware import MatrixKeyboard
import time
import os

BIBLIA_DATA = []
indice_versiculo = 0
precisa_atualizar = True
modo = "menu"  # "menu" ou "leitura"

# Variáveis para paginação do versículo
versiculo_labels = []  # não vamos usar widgets, mas mantém pra referência se quiser adaptar
linhas_versiculo = []
linhas_por_pagina = 6
pagina_versiculo = 0

# Lista de arquivos disponíveis
ARQUIVOS_BIBLIA = [
    'GN.txt', 'EX.txt', 'LV.txt', 'NM.txt', 'DT.txt', 'JS.txt', 'JZ.txt', 'RT.txt', '1SM.txt', '2SM.txt',
    '1RS.txt', '2RS.txt', '1CR.txt', '2CR.txt', 'ED.txt', 'NE.txt', 'ET.txt', 'Jó.txt', 'SL.txt', 'PV.txt',
    'EC.txt', 'CT.txt', 'IS.txt', 'JR.txt', 'LM.txt', 'EZ.txt', 'DN.txt', 'OS.txt', 'JL.txt', 'AM.txt',
    'OB.txt', 'JN.txt', 'MQ.txt', 'NA.txt', 'HC.txt', 'SF.txt', 'AG.txt', 'ZC.txt', 'ML.txt',
    'MT.txt', 'MC.txt', 'LC.txt', 'JO.txt', 'AT.txt', 'RM.txt', '1CO.txt', '2CO.txt', 'GL.txt', 'EF.txt',
    'FP.txt', 'CL.txt', '1TS.txt', '2TS.txt', '1TM.txt', '2TM.txt', 'TT.txt', 'FM.txt', 'HB.txt', 'TG.txt',
    '1PE.txt', '2PE.txt', '1JO.txt', '2JO.txt', '3JO.txt', 'JD.txt', 'AP.txt'
]

arquivo_selecionado_index = 0

def carregar_biblia_do_arquivo(nome_arquivo):
    global BIBLIA_DATA
    BIBLIA_DATA.clear()
    try:
        with open('/flash/' + nome_arquivo, 'r') as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue
                partes = linha.split(',', 3)
                if len(partes) != 4:
                    continue
                livro, cap_str, vers_str, texto = partes
                try:
                    cap = int(cap_str)
                    vers = int(vers_str)
                except:
                    continue
                BIBLIA_DATA.append([livro, cap, vers, texto])
    except Exception as e:
        print("Erro ao carregar arquivo: ", e)

def voltar_ao_menu():
    global modo, indice_versiculo, BIBLIA_DATA, precisa_atualizar, pagina_versiculo, linhas_versiculo
    modo = "menu"
    indice_versiculo = 0
    BIBLIA_DATA.clear()
    linhas_versiculo.clear()
    pagina_versiculo = 0
    precisa_atualizar = True

def remover_acentos(texto):
    mapa = {
        'á':'a', 'à':'a', 'ã':'a', 'â':'a',
        'é':'e', 'ê':'e',
        'í':'i',
        'ó':'o', 'ô':'o', 'õ':'o',
        'ú':'u',
        'ç':'c',
        'Á':'A', 'À':'A', 'Ã':'A', 'Â':'A',
        'É':'E', 'Ê':'E',
        'Í':'I',
        'Ó':'O', 'Ô':'O', 'Õ':'O',
        'Ú':'U',
        'Ç':'C'
    }
    return ''.join(mapa.get(c, c) for c in texto)


def mostrar_menu_arquivos():
    M5.Lcd.fillScreen(0)
    M5.Lcd.setTextSize(1)
    M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
    M5.Lcd.setCursor(10, 10)
    M5.Lcd.print("Escolha o arquivo:")

    itens_por_pagina = 6
    pagina = arquivo_selecionado_index // itens_por_pagina
    inicio = pagina * itens_por_pagina
    fim = min(inicio + itens_por_pagina, len(ARQUIVOS_BIBLIA))

    y = 45
    for i in range(inicio, fim):
        if i == arquivo_selecionado_index:
            M5.Lcd.fillRect(10, y - 5, 200, 20, 0x5555FF)  # Destaque
            M5.Lcd.setTextColor(0xFFFFFF, 0x5555FF)
        else:
            M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
        M5.Lcd.setCursor(20, y)
        prefix = "> " if i == arquivo_selecionado_index else "  "
        M5.Lcd.print(prefix + ARQUIVOS_BIBLIA[i])
        y += 25

def preparar_versiculo_paginado(indice):
    global linhas_versiculo, pagina_versiculo

    if indice < 0 or indice >= len(BIBLIA_DATA):
        linhas_versiculo = ["Fim da Bíblia"]
    else:
        vers = BIBLIA_DATA[indice]
        texto = remover_acentos(vers[3])  # <-- aqui, removendo acentos
        max_chars = 25
        linhas_versiculo = []
        linha_atual = ""
        for palavra in texto.split():
            if len(linha_atual) + len(palavra) + 1 <= max_chars:
                linha_atual += (palavra + " ")
            else:
                linhas_versiculo.append(linha_atual.strip())
                linha_atual = palavra + " "
        if linha_atual:
            linhas_versiculo.append(linha_atual.strip())
    pagina_versiculo = 0
    mostrar_versiculo_pagina(pagina_versiculo)

def mostrar_versiculo_pagina(pagina):
    global linhas_versiculo, linhas_por_pagina

    M5.Lcd.fillScreen(0x000000)
    M5.Lcd.setTextSize(1)  # fonte menor
    M5.Lcd.setTextColor(0xFFFFFF, 0x000000)

    inicio = pagina * linhas_por_pagina
    fim = inicio + linhas_por_pagina
    linhas_para_mostrar = linhas_versiculo[inicio:fim]

    y = 10
    for linha in linhas_para_mostrar:
        M5.Lcd.setCursor(10, y)
        M5.Lcd.print(linha)
        y += 15  # reduzir espaçamento vertical para caber mais linhas

    # Mostrar referência do versículo
    if BIBLIA_DATA and 0 <= indice_versiculo < len(BIBLIA_DATA):
        vers = BIBLIA_DATA[indice_versiculo]
        ref = f"{vers[0]} {vers[1]}:{vers[2]}"
        M5.Lcd.setCursor(10, 0)
        M5.Lcd.print(ref)

    # Desenha setas para navegação entre páginas do versículo
    largura = 176
    if pagina > 0:
        M5.Lcd.setCursor(largura - 10, y)
        M5.Lcd.print("^")
    if fim < len(linhas_versiculo):
        M5.Lcd.setCursor(largura - 10, y + 12)
        M5.Lcd.print("v")

def kb_pressed_event(kb):
    global indice_versiculo, precisa_atualizar, modo, arquivo_selecionado_index, pagina_versiculo

    key = kb.get_key()
    if key is None:
        return

    if modo == "menu":
        if key == 46:  # Seta para baixo
            arquivo_selecionado_index = (arquivo_selecionado_index + 1) % len(ARQUIVOS_BIBLIA)
            precisa_atualizar = True
        elif key == 59:  # Seta para cima
            arquivo_selecionado_index = (arquivo_selecionado_index - 1) % len(ARQUIVOS_BIBLIA)
            precisa_atualizar = True
        elif key == 13:  # ENTER
            carregar_biblia_do_arquivo(ARQUIVOS_BIBLIA[arquivo_selecionado_index])
            modo = "leitura"
            indice_versiculo = 0
            preparar_versiculo_paginado(indice_versiculo)
            precisa_atualizar = False  # já atualizou na preparação

    elif modo == "leitura":
        if key == 46:  # Seta para baixo
            # Tenta avançar a página do versículo
            if (pagina_versiculo + 1) * linhas_por_pagina < len(linhas_versiculo):
                pagina_versiculo += 1
                mostrar_versiculo_pagina(pagina_versiculo)
            else:
                # Se não tem mais páginas, vai para próximo versículo
                if indice_versiculo < len(BIBLIA_DATA) - 1:
                    indice_versiculo += 1
                    preparar_versiculo_paginado(indice_versiculo)
            precisa_atualizar = False

        elif key == 59:  # Seta para cima
            # Tenta voltar página do versículo
            if pagina_versiculo > 0:
                pagina_versiculo -= 1
                mostrar_versiculo_pagina(pagina_versiculo)
            else:
                # Se estiver na primeira página, volta para versículo anterior
                if indice_versiculo > 0:
                    indice_versiculo -= 1
                    preparar_versiculo_paginado(indice_versiculo)
            precisa_atualizar = False

        elif key == 27:  # ESC volta ao menu
            voltar_ao_menu()

def setup():
    global kb
    M5.begin()
    kb = MatrixKeyboard()
    kb.set_callback(kb_pressed_event)
    mostrar_menu_arquivos()

def loop():
    global precisa_atualizar
    kb.tick()
    M5.update()
    if precisa_atualizar:
        if modo == "menu":
            mostrar_menu_arquivos()
        elif modo == "leitura":
            mostrar_versiculo_pagina(pagina_versiculo)
        precisa_atualizar = False
    if M5.BtnA.wasPressed():
        voltar_ao_menu()

if __name__ == "__main__":
    setup()
    while True:
        loop()
        time.sleep(0.1)
