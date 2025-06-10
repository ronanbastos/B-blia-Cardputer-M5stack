import re
import json

with open("biblia.txt", "r", encoding="utf-8") as f:
    linhas = f.readlines()

# Dicionário das siglas (com números arábicos e romanos convertidos)
siglas = {
    "GENESIS": "GN",
    "GÊNESIS": "GN",
    "ÊXODO": "EX",
    "LEVÍTICO": "LV",
    "NÚMEROS": "NM",
    "DEUTERONÔMIO": "DT",
    "JOSUÉ": "JS",
    "JUÍZES": "JZ",
    "RUTE": "RT",
    "1 SAMUEL": "1SM",
    "2 SAMUEL": "2SM",
    "1 REIS": "1RS",
    "2 REIS": "2RS",
    "1 CRÔNICAS": "1CR",
    "2 CRÔNICAS": "2CR",
    "ESDRAS": "EDR",
    "NEEMIAS": "NEE",
    "ESTER": "EST",
    "JÓ": "JO",
    "SALMOS": "SL",
    "PROVÉRBIOS": "PV",
    "ECLESIASTES": "EC",
    "CÂNTICOS": "CT",
    "ISAÍAS": "IS",
    "JEREMIAS": "JR",
    "LAMENTAÇÕES": "LM",
    "EZEQUIEL": "EZ",
    "DANIEL": "DN",
    "OSÉIAS": "OS",
    "JOEL": "JL",
    "AMOS": "AM",
    "OBADIAS": "OB",
    "JONAS": "JN",
    "MICAIAS": "MC",
    "NAUM": "NA",
    "HABACUC": "HC",
    "SOFONIAS": "SF",
    "AGEU": "AG",
    "ZACARIAS": "ZC",
    "MALAQUIAS": "ML",
    "MATEUS": "MT",
    "MARCOS": "MC",
    "LUCAS": "LC",
    "JOÃO": "JO",
    "ATOS": "AT",
    "ROMANOS": "RM",
    "1 CORÍNTIOS": "1CO",
    "2 CORÍNTIOS": "2CO",
    "GÁLATAS": "GL",
    "EFÉSIOS": "EF",
    "FILIPENSES": "FP",
    "COLOSSENSES": "CL",
    "1 TESSALONICENSES": "1TS",
    "2 TESSALONICENSES": "2TS",
    "1 TIMÓTEO": "1TM",
    "2 TIMÓTEO": "2TM",
    "TITO": "TT",
    "FILEMON": "FM",
    "HEBREUS": "HB",
    "TIAGO": "TG",
    "1 PEDRO": "1PE",
    "2 PEDRO": "2PE",
    "1 JOÃO": "1JO",
    "2 JOÃO": "2JO",
    "3 JOÃO": "3JO",
    "JUDAS": "JD",
    "APOCALIPSE": "AP",

    # Versões com números romanos para 1,2,3 convertidos para números arábicos
    "I PEDRO": "1PE",
    "II PEDRO": "2PE",
    "III JOÃO": "3JO",
    "I JOÃO": "1JO",
    "II JOÃO": "2JO",
    "III JOÃO": "3JO",
    "I CORÍNTIOS": "1CO",
    "II CORÍNTIOS": "2CO",
    "I SAMUEL": "1SM",
    "II SAMUEL": "2SM",
    "I REIS": "1RS",
    "II REIS": "2RS",
    "I CRÔNICAS": "1CR",
    "II CRÔNICAS": "2CR",
    "I TESSALONICENSES": "1TS",
    "II TESSALONICENSES": "2TS",
    "I TIMÓTEO": "1TM",
    "II TIMÓTEO": "2TM",
}

def converter_roman_to_arabic(romano):
    romanos = {'I': 1, 'II': 2, 'III': 3}
    return romanos.get(romano, None)

BIBLIA_DATA = []
livro_atual = ""
capitulo_atual = 0

for linha in linhas:
    linha = linha.strip()
    if not linha:
        continue

    # Captura linha com livro e capítulo:
    # Exemplo: "II PEDRO 3" ou "1 CORÍNTIOS 13" ou "JOÃO 3"
    match = re.match(r"^([IVX]+|[1-3])?\s*([A-ZÇÁÉÍÓÚÂÊÔÃ ]+)\s+(\d+)$", linha.upper())

    if match:
        num_romano_ou_arabico = match.group(1) or ""
        nome_livro = match.group(2).strip()
        capitulo_atual = int(match.group(3))

        if num_romano_ou_arabico in ["I", "II", "III"]:
            numero = converter_roman_to_arabic(num_romano_ou_arabico)
            chave_livro = f"{numero} {nome_livro}"
        elif num_romano_ou_arabico in ["1", "2", "3"]:
            chave_livro = f"{num_romano_ou_arabico} {nome_livro}"
        else:
            chave_livro = nome_livro

        # pegar sigla do dicionário, ou pegar primeiros 2 chars
        livro_atual = siglas.get(chave_livro, chave_livro[:2])
        continue

    # Captura versículo
    match_vers = re.match(r"^(\d+)\s+(.*)", linha)
    if match_vers and livro_atual and capitulo_atual:
        versiculo = int(match_vers.group(1))
        texto = match_vers.group(2).strip()
        BIBLIA_DATA.append([livro_atual, capitulo_atual, versiculo, texto])

with open("biblia_data.json", "w", encoding="utf-8") as out:
    json.dump(BIBLIA_DATA, out, ensure_ascii=False, indent=2)

print("✅ Bíblia convertida com sucesso para estrutura de listas!")
