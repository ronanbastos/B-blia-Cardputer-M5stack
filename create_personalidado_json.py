import json
from collections import defaultdict

# Carrega os dados da Bíblia
with open("biblia_data.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

# Agrupa os versículos por livro
livros_dict = defaultdict(list)
for versiculo in data:
    livro = versiculo[0]
    livros_dict[livro].append(versiculo)

# Para cada livro, ordena e salva em um arquivo separado
for livro, versos in livros_dict.items():
    versos_ordenados = sorted(versos, key=lambda x: (x[1], x[2]))  # capítulo, versículo

    filename = f"{livro}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(versos_ordenados, f, ensure_ascii=False, indent=2)

    print(f"{len(versos_ordenados)} versículos do livro {livro} salvos em '{filename}'")
