import re
from app.datastore.datastore import Datastore
from app.models.attempt import Attempt
from app.models.choice_algorithm import ChoiceAlgorithm
from app.services.usecases import gen_patterns
from app.utils.logger import log


class WordMgr:

    def __init__(self, choice_algorithm: ChoiceAlgorithm, datastore: Datastore):
        self._words = []
        self._choice_algorithm = choice_algorithm
        self._datastore = datastore
        self._words = datastore.get()
    
    def get_offer(self) -> str:
        log("WordMgr::get_offer", 30)
        self._choice_algorithm.process(self._words)

        return self._choice_algorithm.get_choice()
    
    def get_next_offer(self) -> str:
        log("WordMgr::get_next_offer", 30)

        return self._choice_algorithm.get_choice()
    
    def process_attempt(self, attempt: Attempt) -> None:
        log("WordMgr::process_attempt", 30)
        patterns = gen_patterns(attempt)
        for pattern in patterns:
            self._words = list(filter(lambda w: re.search(pattern, w) is not None, self._words))
    
    def is_equal_base(self, words: list[str]) -> bool:
        log(" ".join(self._words))

        return words == self._words
