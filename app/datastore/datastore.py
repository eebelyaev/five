from app.config.config import WORD_5_FILE
from app.utils.logger import log


class Datastore:
    
    def __init__(self):
        self._words = []
    
    def load(self) -> None:
        log("Datastore::load", 30)
        with open(WORD_5_FILE, "r", encoding='utf-8') as f:
            self._words = [word.removesuffix("\n") for word in f.readlines()] #[:1000]
        log(f"Всего слов: {len(self._words)}", 20)

    def get(self) -> list[str]:
        log("Datastore::get", 30)
        return self._words.copy()        
    
    def set(self, words: list[str]) -> None:
        log("Datastore::set", 30)
        self._words = words
        log(f"Всего слов: {len(self._words)}", 20)
