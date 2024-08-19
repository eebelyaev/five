from app.utils.logger import log


class StatMgr:
    '''Накапливает статистику по работе алгоритмов.'''

    def __init__(self) -> None:
        self._chain_len_counts: dict[int, int] = {}
        self._words_big_chain: dict[str, int] = {}

    def add_game_info(self, word: str, len_chain: int):
        '''Сохраняет информацию об игре.
        
        word - угадываемое слово;

        len_chain - требующееся количество попыток.'''

        if len_chain in self._chain_len_counts:
            self._chain_len_counts[len_chain] += 1
        else:
            self._chain_len_counts[len_chain] = 1

        if len_chain >= 10:
            self._words_big_chain[word] = len_chain

    def print_chain_len_counts(self):
        log(f"Распределение слов по длине цепочки", 5)
        for key in sorted(self._chain_len_counts.keys()):
            log(f"{key}: {self._chain_len_counts[key]}", 5)

    def print_words_big_chain(self):
        log(f"Цепочки максимальной длины", 5)
        for key in sorted(self._words_big_chain, key=self._words_big_chain.get):
            log(f"{key}: {self._words_big_chain[key]}", 5)
