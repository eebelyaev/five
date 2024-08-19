import app.models.choice_algorithm as choice
from app.datastore.datastore import Datastore
from app.models.game import Game
from app.models.player import Player
from app.models.word_mgr import WordMgr
from app.services.stat_mgr import StatMgr
from app.utils.logger import log


def play(game: Game, player: Player) -> int:    
    log("Start game", 10, True)
    for i in range(20):
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

    player = Player(choice_algorithm, datastore, confirm)
    game = Game(word)
    _ = play(game, player)


def play_all_words(choice_algorithm: choice.ChoiceAlgorithm):
    datastore = Datastore()
    datastore.load()

    word_mgr = WordMgr(choice.ChoiceAlgorithmFirst(), datastore)
    word = word_mgr.get_offer()
    stat_mgr = StatMgr()

    log(choice_algorithm.__repr__(), 5, True)
    while word != "":
        player = Player(choice_algorithm, datastore)
        game = Game(word)
        len_chain = play(game, player)

        stat_mgr.add_game_info(word, len_chain)
        word = word_mgr.get_next_offer()

    stat_mgr.print_chain_len_counts()
    stat_mgr.print_words_big_chain()
