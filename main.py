import app.models.choice_algorithm as choice
from app.services.play import play_all_words, play_one
from app.utils.logger import log


if __name__ == "__main__":

    log("Start", is_tstamp=True)
    play_all_words(choice.ChoiceAlgorithmVerySmart())
    log("Finish", is_tstamp=True)
