import app.models.choice_algorithm as choice
from app.datastore.datastore import Datastore
from app.models.game import Game
from app.models.player import Player
from app.models.word_mgr import WordMgr
from app.utils.logger import log


def play(game: Game, player: Player) -> int:    
    log("Start game", 10, True)
    for i in range(100):
        word = player.offer_word()
        if word == "":
            log("play: player.offer_word вернул пустую строку!")
            return 0
        
        log(f"Попытка №{i+1}: {word}", 10)
        mask = game.get_mask(word)
        log(f"{word} {mask}", 20)
        if mask == "11111":
            log(f"Слово разгадано: {word}", 10)
            log(f"Потребовалось попыток: {game.attempt_count()}", 10)
            break
        player.receive_mask(mask)
    attempt_count = game.attempt_count()
    log("Finish game", 10, True)

    return attempt_count


def play_one(word: str, 
            choice_algorithm: choice.ChoiceAlgorithm, 
            confirm: bool = False):
    datastore = Datastore()
    datastore.load()

    player = Player(choice_algorithm, datastore)
    player.confirm_offer = confirm
    game = Game(word)
    _ = play(game, player)


def play_all_words(choice_algorithm: choice.ChoiceAlgorithm):
    datastore = Datastore()
    datastore.load()

    mgr = WordMgr(choice.ChoiceAlgorithmFirst(), datastore)
    word = mgr.get_offer()
    chain_len_counts: dict[int, int] = {}
    words_big_chain: dict[str, int] = {}
    log(choice_algorithm.__repr__(), 5, True)
    while word != "":
        player = Player(choice_algorithm, datastore)
        game = Game(word)
        len_chain = play(game, player)
        _add_chain_len_counts(chain_len_counts, len_chain)
        _add_words_big_chain(words_big_chain, word, len_chain)
        word = mgr.get_next_offer()

    _print_chain_len_counts(chain_len_counts)
    _print_words_big_chain(words_big_chain)

def _add_chain_len_counts(chain_len_counts: dict[int, int], len_chain: int):
    if len_chain in chain_len_counts:
        chain_len_counts[len_chain] += 1
    else:
        chain_len_counts[len_chain] = 1

def _add_words_big_chain(words_big_chain: dict[str, int], word: str, len_chain: int):
    if len_chain >= 10:
        words_big_chain[word] = len_chain
        # log(f"{word}: {len_chain}", 5)

def _print_chain_len_counts(chain_len_counts: dict[int, int]):
    log(f"Распределение слов по длине цепочки:", 5)
    for key in sorted(chain_len_counts.keys()):
        log(f"{key}: {chain_len_counts[key]}", 5)

def _print_words_big_chain(words_big_chain: dict[str, int]):
    log(f"Цепочки максимальной длины:", 5)
    for key in sorted(words_big_chain, key=words_big_chain.get):
        log(f"{key}: {words_big_chain[key]}", 5)
