from app.config.config import ALFABET, WL
from app.models.attempt import Attempt


def gen_patterns(attempt: Attempt) -> list[str]:
    '''Генерирует паттерны для поиска слов в базе.
    '''

    letters = [ALFABET] * WL
    mask_2_groups = []
    for i in range(WL):
        ch = attempt.word[i]
        match attempt.mask[i]:
            case "0":
                for j in range(WL):
                    if attempt.mask[j] != "1":
                        letters[j] = letters[j].replace(ch, "")
            case "1":
                letters[i] = ch
            case _:
                letters[i] = letters[i].replace(ch, "")
                # Буква обязательно содержится на некоторых местах с маской 0 и 2
                for j in range(WL):
                    if attempt.mask[j] != "1" and i != j:
                        group = "."*j + ch + "."*(WL - j - 1)
                        mask_2_groups.append(f"({group})")

    pattern = ""
    for letter in letters:
        pattern += f"[{letter}]"

    patterns = [pattern]
    if len(mask_2_groups) > 0:
        patterns.append("|".join(mask_2_groups))

    return patterns

def calc_mask(hword: str, word: str) -> str:
    mask = ""
    for i in range(WL):
        c = word[i]
        if c == hword[i]:
            mask += "1"
        else:
            in_another_place = False
            for j in range(WL):
                if i != j and hword[j] == c and word[j] != c:
                    in_another_place = True
                    break
                
            mask += "2" if in_another_place else "0"
    
    return mask
            
def count_letter_frequencies(words: list[str]) -> dict[str, int]:
    letter_count = {}
    for word in words:
        for letter in word:
            if letter in letter_count:
                letter_count[letter] += 1
            else:
                letter_count[letter] = 1

    return letter_count

def reset_used_letters(letter_count: dict[str, int], used_letters: str):
    for letter in used_letters:
        letter_count[letter] = 0

def sum_letter_values(words: list[str], letter_count: dict[str, int]) -> dict[str, int]:
    word_weights = {}
    for word in words:
        total_value = sum(letter_count.get(letter, 0) for letter in word)
        word_weights[word] = total_value

    return word_weights

def smart_sum_letter_values(words: list[str], letter_count: dict[str, int]) -> dict[str, int]:
    word_weights = {}
    for word in words:
        short_word = remove_duplicates(word)
        total_value = sum(letter_count.get(letter, 0) for letter in short_word)
        word_weights[word] = total_value

    return word_weights

def add_weights(weights: dict[str, int], delta: int, all_weights: dict[str, int]) -> None:
    '''Добавляет в all_weights веса из weights. К весу предварительно добавляет delta.
    Если в all_weights вес для слова меньше, чем рассчитанный вес.'''
    for key, value in weights.items():
        v = all_weights.get(key, 0)
        value += delta
        if value > v:
            all_weights[key] = value

def sort_words_by_value(word_weights: dict[str, int]) -> list[str]:
    sorted_words = sorted(word_weights.items(), key=lambda item: item[1], reverse=True)
    words = [word for word, _ in sorted_words]

    return words

def remove_duplicates(s: str) -> str:
    unique_chars = []
    for char in s:
        if char not in unique_chars:
            unique_chars.append(char)
    
    return ''.join(unique_chars)