import pytest
from app.models.attempt import Attempt
from app.models.choice_algorithm import ChoiceAlgorithm
from app.datastore.datastore import Datastore
from app.models.word_mgr import WordMgr
from app.utils.logger import log


class TestWordMgr:
    
    def test_process_attempt(self):
        words = ["абвгд", "саоди", "саодо", "саокл", "саовт", "саово", "саовл", "саолу", "саоло", "саолв", "саолл", "слово", "ежзик", "филин"]
        masks = ["00200", "10100", "10101", "10102", "10110", "10111", "10112", "10120", "10121", "10122", "10122", "11111", "00000", "00200"]
        expected_words = [
            ["слово"], # "абвгд"
            ["слово"], # "саоди"
            ["слово"], # "саодо"
            ["слово"], # "саокл"
            ["слово"], # "саовт"
            ["слово"], # "саово"
            ["слово"], # "саовл"
            ["слово"], # "саолу"
            ["слово"], # "саоло"
            ["слово"], # "саолв"
            ["слово"], # "саолл"
            ["слово"], # "слово"
            ["абвгд", "саодо", "саовт", "саово", "саовл", "саолу", "саоло", "саолв", "саолл", "слово"], # "ежзик"
            ["саокл", "саовл", "саолу", "саоло", "саолв", "саолл", "слово"] # "филин"
        ]

        datastore = Datastore()
        datastore.set(words)
        for i in range(len(words)):
            mgr = WordMgr(ChoiceAlgorithm, datastore)
            mgr.process_attempt(Attempt(words[i], masks[i]))

            log(Attempt(words[i], masks[i]).__repr__())
            assert mgr.is_equal_base(expected_words[i])
        
                    
if __name__ == '__main__':
    pytest.main()
