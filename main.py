import app.models.choice_algorithm as choice
from app.services.play import play_all_words, play_one
from app.utils.logger import log


if __name__ == "__main__":
    # play_one("арбуз", choice.ChoiceAlgorithmSmart())
    
    log("Start", is_tstamp=True)
    play_all_words(choice.ChoiceAlgorithmSmart())
    play_all_words(choice.ChoiceAlgorithmFirst())
    play_all_words(choice.ChoiceAlgorithmRandom())
    play_all_words(choice.ChoiceAlgorithmAlmostSmart())
    play_all_words(choice.ChoiceAlgorithmAlmostSmartRevert())
    play_all_words(choice.ChoiceAlgorithmSmartRevert())
    log("Finish", is_tstamp=True)
