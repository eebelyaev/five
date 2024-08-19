from app.models.attempt import Attempt
from app.models.choice_algorithm import ChoiceAlgorithm, ChoiceAlgorithmVerySmart
from app.datastore.datastore import Datastore
from app.models.word_mgr import WordMgr
from app.utils.logger import log


class Player:
    
    def __init__(self, choice_algorithm: ChoiceAlgorithm, 
                 datastore: Datastore, 
                 confirm_offer: bool = False):
        self._attempt = Attempt()
        self._word_mgr = WordMgr(choice_algorithm, datastore)
        self._confirm_offer = confirm_offer
    
    def offer_word(self) -> str:
        log("Player::offer_word", 20)
        word = self._word_mgr.get_offer()
        while True:
            log(f"Предложенное слово: {word}", 10)
            if self._confirm_offer:
                answer = input("Слово понравилось? (y/n/o): ").strip().lower()
                if answer == 'o':
                    word = input("Введите слово: ")
                    break
                else:
                    if answer == 'y':
                        break
            else:
                break

            word = self._word_mgr.get_next_offer()

        self._attempt.word = word

        return word

    def receive_mask(self, mask: str) -> None:
        log(f"Player::receive_mask({mask})", 20)
        self._attempt.mask = mask
        self._word_mgr.process_attempt(self._attempt)
