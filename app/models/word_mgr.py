import re
from app.datastore.datastore import Datastore
from app.models.attempt import Attempt
from app.models.choice_algorithm import ChoiceAlgorithm
from app.models.choice_data import ChoiceData
from app.services.usecases import gen_patterns
from app.utils.logger import log


class WordMgr:

    def __init__(self, choice_algorithm: ChoiceAlgorithm, datastore: Datastore):
        self._words = []
        self._choice_algorithm = choice_algorithm
        self._words = datastore.get()
        self._all_words = datastore.get()
        self._used_letters = ""
    
    def get_offer(self) -> str:
        log("WordMgr::get_offer", 30)
        if len(self._words) == 1:
            return self._words[0]
        
        choice_data = ChoiceData()
        choice_data.words = self._words
        choice_data.all_words = self._all_words
        choice_data.used_letters = self._used_letters
        choice_data.delta = 10
        
        self._choice_algorithm.process(choice_data)

        return self._choice_algorithm.get_choice()
    
    def get_next_offer(self) -> str:
        log("WordMgr::get_next_offer", 30)

        return self._choice_algorithm.get_choice()
    
    def process_attempt(self, attempt: Attempt) -> None:
        log("WordMgr::process_attempt", 30)
        patterns = gen_patterns(attempt)
        for pattern in patterns:
            self._words = list(filter(lambda w: re.search(pattern, w) is not None, self._words))
        
        for letter in attempt.word:
            if letter not in self._used_letters:
                self._used_letters += letter

    def is_equal_base(self, words: list[str]) -> bool:
        log(" ".join(self._words))

        return words == self._words

    def word_base_size(self) -> int:
        return len(self._words)