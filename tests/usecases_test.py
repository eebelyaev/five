import pytest

from app.models.attempt import Attempt
from app.services.usecases import calc_mask, gen_patterns, remove_duplicates, smart_sum_letter_values, sum_letter_values


class TestUsecases:

    def test_gen_patterns(self):

        attempts = [
            Attempt("абвгд", "00000"),
            Attempt("абвгд", "00002"),
            Attempt("абвгд", "00022"),
        ]
        expected = [
            [
                "[ежзийклмнопрстуфхцчшщьыъэюя][ежзийклмнопрстуфхцчшщьыъэюя][ежзийклмнопрстуфхцчшщьыъэюя][ежзийклмнопрстуфхцчшщьыъэюя][ежзийклмнопрстуфхцчшщьыъэюя]",
            ],
            [
                "[дежзийклмнопрстуфхцчшщьыъэюя][дежзийклмнопрстуфхцчшщьыъэюя][дежзийклмнопрстуфхцчшщьыъэюя][дежзийклмнопрстуфхцчшщьыъэюя][ежзийклмнопрстуфхцчшщьыъэюя]",
                "(д....)|(.д...)|(..д..)|(...д.)"
            ],
            [
                "[гдежзийклмнопрстуфхцчшщьыъэюя][гдежзийклмнопрстуфхцчшщьыъэюя][гдежзийклмнопрстуфхцчшщьыъэюя][дежзийклмнопрстуфхцчшщьыъэюя][гежзийклмнопрстуфхцчшщьыъэюя]",
                "(г....)|(.г...)|(..г..)|(....г)|(д....)|(.д...)|(..д..)|(...д.)"
            ]
        ]

        for i in range(len(attempts)):
            actual_patterns = gen_patterns(attempts[i])
            actual_len = len(actual_patterns)

            assert actual_len == len(expected[i])
            for j in range(actual_len):
                assert actual_patterns[j] == expected[i][j]
    
    def test_calc_mask(self):
        hword = "слово"
        words = ["абвгд", "саоди", "саодо", "саокл", "саовт", "саово", "саовл", "саолу", "саоло", "саолв", "саолл", "слово", "словл", "ожовл", "ежзик", "филин"]
        masks = ["00200", "10100", "10101", "10102", "10110", "10111", "10112", "10120", "10121", "10122", "10122", "11111", "11110", "20112", "00000", "00200"]

        for i in range(len(words)):
            assert calc_mask(hword, words[i]) == masks[i]
    
    def test_sum_letter_values(self):
        letter_count = {"а": 4, "р": 2, "к": 1,
                        "н": 2, "б": 1, "с": 1,
                        "л": 1, "о": 2, "в": 1}
        words = ["аркан", "баран", "слово"]
        expected_values = {"аркан": 13, "баран": 13, "слово": 7}
        word_values = sum_letter_values(words, letter_count)
        assert word_values == expected_values

    def test_remove_duplicates(self):
        word = "аркан"
        short_word = remove_duplicates(word)

        assert short_word == "аркн"

    def test_smart_sum_letter_values(self):
        letter_count = {"а": 4, "р": 2, "к": 1,
                        "н": 2, "б": 1, "с": 1,
                        "л": 1, "о": 2, "в": 1}
        words = ["аркан", "баран", "слово"]
        expected_values = {"аркан": 9, "баран": 9, "слово": 5}
        word_values = smart_sum_letter_values(words, letter_count)
        assert word_values == expected_values

                    
if __name__ == '__main__':
    pytest.main()