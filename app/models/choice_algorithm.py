import random

from app.services.usecases import count_letter_frequencies, smart_sum_letter_values, sort_words_by_value, sum_letter_values
from app.utils.logger import log


class ChoiceAlgorithm:

    def __init__(self) -> None:
        self._name = ""

    def __repr__(self) -> str:
        return f"Алгоритм выбора: {self._name}"
    
    def process(self, words: list[str]) -> None:
        pass

    def get_choice(self) -> str:
        return "Hello"

class ChoiceAlgorithmFirst(ChoiceAlgorithm):

    def __init__(self) -> None:
        self._name = "Первый попавшийся"
        self._words = []
        self._run_ind = 0
    
    def process(self, words: list[str]) -> None:
        log("ChoiceAlgorithmFirst::process", 20)
        self._words = words
        self._run_ind = 0

    def get_choice(self) -> str:
        log("ChoiceAlgorithmFirst::get_choice", 20)
        if len(self._words) <= self._run_ind:
            return ""
        word = self._words[self._run_ind]
        self._run_ind += 1

        return word
    
class ChoiceAlgorithmRandom(ChoiceAlgorithm):

    def __init__(self) -> None:
        self._name = "Случайный выбор"

    def process(self, words: list[str]) -> None:
        log("ChoiceAlgorithmRandom::process", 20)
        self._words = words

    def get_choice(self) -> str:
        log("ChoiceAlgorithmRandom::get_choice", 20)
        return random.choice(self._words) if len(self._words) > 0 else ""

class ChoiceAlgorithmAlmostSmart(ChoiceAlgorithmFirst):

    def __init__(self) -> None:
        self._name = "По весу слов"

    def process(self, words: list[str]) -> None:
        log("ChoiceAlgorithmAlmostSmart::process", 20)
        letter_count = count_letter_frequencies(words)
        word_values = sum_letter_values(words, letter_count)
        self._words = sort_words_by_value(word_values)
        self._run_ind = 0

class ChoiceAlgorithmSmart(ChoiceAlgorithmFirst):

    def __init__(self) -> None:
        self._name = "По весу слов без повторений"

    def process(self, words: list[str]) -> None:
        log("ChoiceAlgorithmSmart::process", 20)
        letter_count = count_letter_frequencies(words)
        word_values = smart_sum_letter_values(words, letter_count)
        self._words = sort_words_by_value(word_values)
        self._run_ind = 0

class ChoiceAlgorithmAlmostSmartRevert(ChoiceAlgorithmFirst):

    def __init__(self) -> None:
        self._name = "По весу слов (обратный)"

    def process(self, words: list[str]) -> None:
        log("ChoiceAlgorithmSmartRevert::process", 20)
        letter_count = count_letter_frequencies(words)
        word_values = sum_letter_values(words, letter_count)
        self._words = sort_words_by_value(word_values)
        self._words.reverse()
        self._run_ind = 0

class ChoiceAlgorithmSmartRevert(ChoiceAlgorithmFirst):

    def __init__(self) -> None:
        self._name = "По весу слов без повторений (обратный)"

    def process(self, words: list[str]) -> None:
        log("ChoiceAlgorithmSmartRevert::process", 20)
        letter_count = count_letter_frequencies(words)
        word_values = smart_sum_letter_values(words, letter_count)
        self._words = sort_words_by_value(word_values)
        self._words.reverse()
        self._run_ind = 0
