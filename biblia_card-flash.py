import M5
from M5 import *
from hardware import MatrixKeyboard
import time
import random

# Dados com array bidimensional: [Livro, Capítulo, Versículo, Texto]
BIBLIA_DATA = []

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
                    print("Linha ignorada (formato incorreto):", linha)
                    continue
                livro, cap_str, vers_str, texto = partes
                try:
                    cap = int(cap_str)
                    vers = int(vers_str)
                except:
                    print("Capítulo ou versículo inválido:", linha)
                    continue
                BIBLIA_DATA.append([livro, cap, vers, texto])
        print(f"{len(BIBLIA_DATA)} versículos carregados de {nome_arquivo}")
    except Exception as e:
        print("Erro ao carregar arquivo:", e)

# Exemplo de uso:
carregar_biblia_do_arquivo('pv.txt')


menu_items = ["Pesquisar", "Palavra do dia"]
selected_index = 0
precisa_atualizar = True

label2 = None
label3 = None
kb = None
versiculo_labels = []

modo_pesquisa = False
texto_digitado = ""

pagina_versiculo = 0
linhas_por_pagina = 4
linhas_versiculo = []

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

def draw_menu():
    M5.Lcd.fillScreen(0x000000)
    label2.setVisible(True)
    label3.setVisible(True)
    y = 65
    M5.Lcd.setTextSize(2)
    M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
    for i, item in enumerate(menu_items):
        prefix = "> " if i == selected_index else "  "
        M5.Lcd.setCursor(5, y)
        M5.Lcd.print(prefix + item)
        y += 20

def draw_input():
    M5.Lcd.fillScreen(0x000000)
    M5.Lcd.setTextSize(2)
    M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
    M5.Lcd.setCursor(10, 30)
    M5.Lcd.print("Digite o versiculo:")
    M5.Lcd.setCursor(10, 70)
    M5.Lcd.print(texto_digitado + "_")

def montar_linhas(texto):
    max_chars = 15
    linhas = []
    linha_atual = ""
    for palavra in texto.split():
        if len(linha_atual) + len(palavra) + 1 <= max_chars:
            linha_atual += palavra + " "
        else:
            linhas.append(linha_atual.strip())
            linha_atual = palavra + " "
    linhas.append(linha_atual.strip())
    return linhas

def mostrar_versiculo_pagina(pagina):
    global versiculo_labels, linhas_versiculo, linhas_por_pagina
    for lbl in versiculo_labels:
        lbl.setVisible(False)
    versiculo_labels.clear()
    M5.Lcd.fillScreen(0x000000)

    inicio = pagina * linhas_por_pagina
    fim = inicio + linhas_por_pagina
    linhas_para_mostrar = linhas_versiculo[inicio:fim]

    y = 10
    for linha in linhas_para_mostrar:
        linha_limpa = remover_acentos(linha)
        lbl = Widgets.Label(linha_limpa, 5, y, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.EFontCN24)
        lbl.setVisible(True)
        versiculo_labels.append(lbl)
        y += 26

    M5.Lcd.setTextSize(2)
    M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
    largura = 176
    if pagina > 0:
        M5.Lcd.setCursor(largura - 10, y)
        M5.Lcd.print("^")
    if fim < len(linhas_versiculo):
        M5.Lcd.setCursor(largura - 10, y + 15)
        M5.Lcd.print("v")

def mostrar_versiculo(texto):
    global linhas_versiculo, pagina_versiculo
    linhas_versiculo = montar_linhas(texto)
    pagina_versiculo = 0
    mostrar_versiculo_pagina(pagina_versiculo)

def buscar_versiculo(ref):
    ref = ref.strip().upper()
    if not ref:
        return ["Nenhum versículo digitado."]
    
    partes = ref.split()
    if len(partes) == 1:
        livro = partes[0]
        encontrados = []
        for item in BIBLIA_DATA:
            if item[0] == livro:
                encontrados.append(f"{livro} {item[1]}:{item[2]} - {item[3]}")
        if not encontrados:
            return ["Livro não encontrado."]
        return encontrados

    elif len(partes) == 2:
        livro, resto = partes
        if ":" in resto:
            cap_str, vers_str = resto.split(":")
            try:
                cap = int(cap_str)
                vers = int(vers_str)
            except:
                return ["Formato inválido no capítulo ou versículo."]
            for item in BIBLIA_DATA:
                if item[0] == livro and item[1] == cap and item[2] == vers:
                    return [f"{livro} {cap}:{vers} - {item[3]}"]
            return ["Versículo não encontrado."]
        else:
            try:
                cap = int(resto)
            except:
                return ["Formato inválido no capítulo."]
            encontrados = []
            for item in BIBLIA_DATA:
                if item[0] == livro and item[1] == cap:
                    encontrados.append(f"{livro} {item[1]}:{item[2]} - {item[3]}")
            if not encontrados:
                return ["Capítulo não encontrado."]
            return encontrados

    else:
        return ["Formato inválido. Use: GN, GN 1 ou GN 1:1"]

def palavra_do_dia():
    item = random.choice(BIBLIA_DATA)
    texto = item[3]
    ref = f"{item[0]} {item[1]}:{item[2]}"
    return f"{ref} - {texto}"

def selecionar_opcao():
    global modo_pesquisa, texto_digitado
    opcao = menu_items[selected_index]
    label2.setVisible(False)
    label3.setVisible(False)
    if opcao == "Pesquisar":
        modo_pesquisa = True
        texto_digitado = ""
        draw_input()
    elif opcao == "Palavra do dia":
        texto = palavra_do_dia()
        mostrar_versiculo(texto)

def voltar_ao_menu():
    global modo_pesquisa, texto_digitado, pagina_versiculo, linhas_versiculo
    modo_pesquisa = False
    texto_digitado = ""
    pagina_versiculo = 0
    linhas_versiculo.clear()
    draw_menu()

def kb_pressed_event(kb_0):
    global selected_index, precisa_atualizar, modo_pesquisa, texto_digitado
    global pagina_versiculo, linhas_versiculo, linhas_por_pagina
    KeyCode = kb.get_key()
    if KeyCode is None:
        return

    if KeyCode == 27:  # ESC
        voltar_ao_menu()
        return

    if modo_pesquisa:
        if KeyCode == 13:  # Enter
            modo_pesquisa = False
            resultados = buscar_versiculo(texto_digitado)
            mostrar_versiculo(texto_digitado.upper() + " >>")
            linhas_versiculo.clear()
            for r in resultados:
                linhas_versiculo += montar_linhas(r)
            mostrar_versiculo_pagina(0)
        elif KeyCode == 8:  # Backspace
            if len(texto_digitado) > 0:
                texto_digitado = texto_digitado[:-1]
            draw_input()
        else:
            try:
                if 32 <= KeyCode <= 126:
                    texto_digitado += chr(KeyCode)
                    draw_input()
            except:
                pass
        return

    if linhas_versiculo:
        if KeyCode == 46:  # Seta para baixo
            if (pagina_versiculo + 1) * linhas_por_pagina < len(linhas_versiculo):
                pagina_versiculo += 1
                mostrar_versiculo_pagina(pagina_versiculo)
            return
        elif KeyCode == 59:  # Seta para cima
            if pagina_versiculo > 0:
                pagina_versiculo -= 1
                mostrar_versiculo_pagina(pagina_versiculo)
            return

    if KeyCode == 59:  # Seta para cima no menu
        selected_index = (selected_index - 1) % len(menu_items)
        precisa_atualizar = True
    elif KeyCode == 46:  # Seta para baixo no menu
        selected_index = (selected_index + 1) % len(menu_items)
        precisa_atualizar = True
    elif KeyCode == 13:  # Enter no menu
        selecionar_opcao()

def setup():
    global label2, label3, kb
    M5.begin()
    label2 = Widgets.Label("Bíblia ", 10, 10, 1.0, 0xffffff, 0x222222, Widgets.FONTS.EFontCN24)
    label3 = Widgets.Label("Card †", 50, 30, 1.0, 0xffffff, 0x222222, Widgets.FONTS.EFontCN24)
    kb = MatrixKeyboard()
    kb.set_callback(kb_pressed_event)
    draw_menu()

def loop():
    global precisa_atualizar
    kb.tick()
    M5.update()
    if precisa_atualizar:
        draw_menu()
        precisa_atualizar = False
    if M5.BtnA.wasPressed():
        voltar_ao_menu()

if __name__ == "__main__":
    setup()
    while True:
        loop()
        time.sleep(0.1)
