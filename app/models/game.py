from app.config.config import WL
from app.models.attempt import Attempt
from app.services.usecases import calc_mask
from app.utils.logger import log


class Game:
    
    def __init__(self, hidden_word: str = ""):
        self._hidden_word = hidden_word
        self._attempts: list[Attempt] = []

    def get_mask(self, word: str) -> str:
        '''Возвращает маску совпадений букв с угадываемым словом'''

        log("Game::get_mask", 20)
        mask = ""
        if len(self._hidden_word) == WL:
            mask = calc_mask(self._hidden_word, word)
        else:
            mask = self._input_mask()

        self._attempts.append(Attempt(word, mask))

        return mask
    
    def print_attempts(self):
        for attempt in self._attempts:
            print(f'{attempt.word} {attempt.mask}')
    
    def attempt_count(self) -> int:
        return len(self._attempts)

    def _input_mask(self) -> str:
        while True:
            mask = input("Введите маску из пяти цифр: ")
            if len(mask) != WL or not all(c in '012' for c in mask):
                log("Ошибка: маска должна состоять из пяти цифр от 0 до 2.")
                continue
            break
        
        return mask
