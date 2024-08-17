from app.models.attempt import Attempt
from app.models.choice_algorithm import ChoiceAlgorithm
from app.datastore.datastore import Datastore
from app.models.word_mgr import WordMgr
from app.utils.logger import log


class Player:
    
    def __init__(self, choice_algorithm: ChoiceAlgorithm, datastore: Datastore):
        self._attempt = Attempt()
        self._word_mgr = WordMgr(choice_algorithm, datastore)
        self.confirm_offer = False
    
    def offer_word(self) -> str:
        log("Player::offer_word", 20)
        word = self._word_mgr.get_offer()
        if self.confirm_offer:
            while True:
                if self.confirm_offer:
                    log(f"Предложенное слово: {word}")
                    answer = input("Слово понравилось? (y/n/o): ").strip().lower()
                    if answer == 'o':
                        word = input("Введите слово: ")
                        break
                    else:
                        if answer == 'y':
                            break

                word = self._word_mgr.get_next_offer()

        self._attempt.word = word

        return word

    def receive_mask(self, mask: str) -> None:
        log(f"Player::receive_mask({mask})", 20)
        self._attempt.mask = mask
        self._word_mgr.process_attempt(self._attempt)
