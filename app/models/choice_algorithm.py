import random

from app.models.choice_data import ChoiceData
from app.services.usecases import add_weights, count_letter_frequencies, reset_used_letters, smart_sum_letter_values, sort_words_by_value, sum_letter_values
from app.utils.logger import log


class ChoiceAlgorithm:

    def __init__(self) -> None:
        self._name = ""

    def __repr__(self) -> str:
        return f"Алгоритм выбора: {self._name}"
    
    def process(self, data: ChoiceData) -> None:
        pass

    def get_choice(self) -> str:
        return "Hello"

class ChoiceAlgorithmFirst(ChoiceAlgorithm):

    def __init__(self) -> None:
        self._name = "Первый попавшийся"
        self._words = []
        self._run_ind = 0
    
    def process(self, data: ChoiceData) -> None:
        log("ChoiceAlgorithmFirst::process", 20)
        self._words = data.words
        self._run_ind = 0

    def get_choice(self) -> str:
        log("ChoiceAlgorithmFirst::get_choice", 20)
        if len(self._words) <= self._run_ind:
            self._run_ind = 0
            return ""
        word = self._words[self._run_ind]
        self._run_ind += 1

        return word
    
class ChoiceAlgorithmRandom(ChoiceAlgorithm):

    def __init__(self) -> None:
        self._name = "Случайный выбор"

    def process(self, data: ChoiceData) -> None:
        log("ChoiceAlgorithmRandom::process", 20)
        self._words = data.words

    def get_choice(self) -> str:
        log("ChoiceAlgorithmRandom::get_choice", 20)
        return random.choice(self._words) if len(self._words) > 0 else ""

class ChoiceAlgorithmAlmostSmart(ChoiceAlgorithmFirst):

    def __init__(self) -> None:
        self._name = "По весу слов"

    def process(self, data: ChoiceData) -> None:
        log("ChoiceAlgorithmAlmostSmart::process", 20)
        letter_count = count_letter_frequencies(data.words)
        word_weights = sum_letter_values(data.words, letter_count)
        self._words = sort_words_by_value(word_weights)
        self._run_ind = 0

class ChoiceAlgorithmSmart(ChoiceAlgorithmFirst):

    def __init__(self) -> None:
        self._name = "По весу слов без повторений"

    def process(self, data: ChoiceData) -> None:
        log("ChoiceAlgorithmSmart::process", 20)
        letter_count = count_letter_frequencies(data.words)
        word_weights = smart_sum_letter_values(data.words, letter_count)
        self._words = sort_words_by_value(word_weights)
        self._run_ind = 0

class ChoiceAlgorithmVerySmart(ChoiceAlgorithmFirst):

    def __init__(self) -> None:
        self._name = "По весу всех слов без повторений"

    def process(self, data: ChoiceData) -> None:
        log(f"ChoiceAlgorithmVerySmart::process, len(words): {len(data.words)}, ", 20)
        letter_count = count_letter_frequencies(data.words)
 
        reset_used_letters(letter_count, data.used_letters)
        word_weights = smart_sum_letter_values(data.words, letter_count)
        all_word_weights = smart_sum_letter_values(data.all_words, letter_count)

        add_weights(word_weights, data.delta, all_word_weights)
        self._words = sort_words_by_value(all_word_weights)
        self._run_ind = 0

class ChoiceAlgorithmAlmostSmartRevert(ChoiceAlgorithmFirst):

    def __init__(self) -> None:
        self._name = "По весу слов (обратный)"

    def process(self, data: ChoiceData) -> None:
        log("ChoiceAlgorithmSmartRevert::process", 20)
        letter_count = count_letter_frequencies(data.words)
        word_weights = sum_letter_values(data.words, letter_count)
        self._words = sort_words_by_value(word_weights)
        self._words.reverse()
        self._run_ind = 0

class ChoiceAlgorithmSmartRevert(ChoiceAlgorithmFirst):

    def __init__(self) -> None:
        self._name = "По весу слов без повторений (обратный)"

    def process(self, data: ChoiceData) -> None:
        log("ChoiceAlgorithmSmartRevert::process", 20)
        letter_count = count_letter_frequencies(data.words)
        word_weights = smart_sum_letter_values(data.words, letter_count)
        self._words = sort_words_by_value(word_weights)
        self._words.reverse()
        self._run_ind = 0
