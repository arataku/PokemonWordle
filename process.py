import csv
from typing import Callable
import collections


def remove_all(list, item):
    return [i for i in list if i != item]


def remove_all_by_key(list, key: Callable):
    return [i for i in list if not key(i)]


def process(decided: str, non_decided: list[str], no_use: str):
    aru = "".join(non_decided)
    with open("pokemon_status.csv", "r", encoding="UTF-8") as f:
        reader = [i for i in csv.reader(f)]

    idx1 = reader[0].index("ポケモン名")
    pokemon_list = [i[idx1] for i in reader[1:]]
    pokemon_list = sort_by_appearance(pokemon_list)

    pokemon_list = remove_all_by_key(pokemon_list, lambda x: len(
        x) != 5 or ":" in x or "♀" in x or "♂" in x or "赤" in x or "青" in x or "L" in x or "S" in x)

    for i in range(len(pokemon_list)):
        for j in range(5):
            if decided[j] == "_":
                continue
            if decided[j] != pokemon_list[i][j]:
                pokemon_list[i] = ""
                break
        for j in range(5):
            if pokemon_list[i] == "":
                continue
            if pokemon_list[i][j] in non_decided[j]:
                pokemon_list[i] = ""
                break
        for j in range(len(aru)):
            if pokemon_list[i] == "":
                continue
            if not aru[j] in pokemon_list[i]:
                pokemon_list[i] = ""
                break
        for j in range(len(no_use)):
            if pokemon_list[i] == "":
                continue
            if no_use[j] in pokemon_list[i]:
                pokemon_list[i] = ""
                break
    pokemon_list = remove_all(pokemon_list, "")
    return pokemon_list


def sort_by_appearance(pokemon):
    tmp = "".join(pokemon)
    c = collections.Counter(tmp)
    scores = []
    for value in pokemon:
        score = 0
        c2 = collections.Counter(value)
        for char in value:
            score -= c[char] / c2[char]
        scores.append(score)
    return [i for _, i in sorted(zip(scores, pokemon))]
