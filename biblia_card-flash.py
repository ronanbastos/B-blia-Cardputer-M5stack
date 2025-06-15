import M5
from M5 import *
from hardware import MatrixKeyboard
import time

BIBLIA_DATA = []
indice_versiculo = 0
precisa_atualizar = True

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

def mostrar_versiculo(indice):
    M5.Lcd.fillScreen(0)
    if indice < 0 or indice >= len(BIBLIA_DATA):
        M5.Lcd.setCursor(10, 30)
        M5.Lcd.setTextSize(2)
        M5.Lcd.setTextColor(0xFFFFFF, 0)
        M5.Lcd.print("Fim da Bíblia")
        return
    
    vers = BIBLIA_DATA[indice]
    ref = f"{vers[0]} {vers[1]}:{vers[2]}"
    texto = vers[3]

    M5.Lcd.setTextSize(2)
    M5.Lcd.setTextColor(0xFFFFFF, 0)
    M5.Lcd.setCursor(10, 10)
    M5.Lcd.print(ref)

    M5.Lcd.setTextSize(1)
    linhas = []
    max_chars = 25
    linha_atual = ""
    for palavra in texto.split():
        if len(linha_atual) + len(palavra) + 1 <= max_chars:
            linha_atual += (palavra + " ")
        else:
            linhas.append(linha_atual)
            linha_atual = palavra + " "
    if linha_atual:
        linhas.append(linha_atual)

    y = 40
    for l in linhas:
        M5.Lcd.setCursor(10, y)
        M5.Lcd.print(l)
        y += 12

def kb_pressed_event(kb):
    global indice_versiculo, precisa_atualizar

    key = kb.get_key()
    if key is None:
        return
    
    if key == 59:  # Seta para cima
        if indice_versiculo > 0:
            indice_versiculo -= 1
            precisa_atualizar = True
    elif key == 46:  # Seta para baixo
        if indice_versiculo < len(BIBLIA_DATA) - 1:
            indice_versiculo += 1
            precisa_atualizar = True
    elif key == 27:  # ESC para voltar ao menu ou reiniciar
        indice_versiculo = 0
        precisa_atualizar = True

def setup():
    global kb
    M5.begin()
    carregar_biblia_do_arquivo('data.txt')
    kb = MatrixKeyboard()
    kb.set_callback(kb_pressed_event)
    mostrar_versiculo(indice_versiculo)

def loop():
    global precisa_atualizar
    kb.tick()
    M5.update()
    if precisa_atualizar:
        mostrar_versiculo(indice_versiculo)
        precisa_atualizar = False

if __name__ == "__main__":
    setup()
    while True:
        loop()
        time.sleep(0.1)
