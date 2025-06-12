import json

# Abrir o arquivo original
with open("biblia_data.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

# Lista com os 27 do Novo Testamento + Provérbios e Salmos
livros_desejados = [
    "MT", "MC", "LC", "JO", "AT",
    "RM", "1CO", "2CO", "GL", "EF", "FP", "CL",
    "1TS", "2TS", "1TM", "2TM", "TT", "FM",
    "HB", "TG", "1PE", "2PE", "1JO", "2JO", "3JO", "JD", "AP",
    "PV", "SL"
]

# Filtrar os versículos
versiculos_filtrados = [verso for verso in data if verso[0] in livros_desejados]

# Salvar no mesmo formato
with open("nt_pv_sl.txt", "w", encoding="utf-8") as f:
    json.dump(versiculos_filtrados, f, ensure_ascii=False, indent=2)

print(f"{len(versiculos_filtrados)} versículos salvos em 'nt_pv_sl.txt'")
