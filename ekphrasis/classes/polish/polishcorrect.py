import re
from collections import Counter
from typing import Dict, List

from unidecode import unidecode

from ekphrasis.classes.polish.badwords import BadwordDetector
from ekphrasis.utils.helpers import read_stats, case_of

REGEX_TOKEN = re.compile(r'\b[^\W\d_]{2,}\b', re.UNICODE)
REGEX_TYPOS = re.compile(r'((.)\2+|h|ch|z|ż|rz|u|ó)', re.UNICODE)

TYPO_MAPPING = {
    "h": ["h", "ch"],
    "ch": ["h", "ch"],
    "z": ["ż", "ź", "rz"],
    "ż": ["rz", "ż"],
    "u": ["ó", "u"],
    "ó": ["ó", "u"]
}

class PolishCorrector:

    def __init__(self, corpus="polish"):
        super().__init__()
        self.WORDS: Counter = corpus if isinstance(corpus, Counter) else Counter(read_stats(corpus, 1))
        self.NOACCENT: Dict[str, str] = self.__prepare_noaccent()
        self.N: int = sum(self.WORDS.values())
        self.badword_detector = BadwordDetector(self.WORDS)

    def __prepare_noaccent(self):
        res = {}
        for word in self.WORDS.keys():
            base = unidecode(word)
            other = res.get(base, None)
            if other is None or self.WORDS[word] > self.WORDS[other]:
                res[base] = word
        return res

    def __find_word(self, word):
        if word in self.WORDS: return word
        elif word in self.NOACCENT: return self.NOACCENT[word]
        else: return None

    @staticmethod
    def get_possible_corrections(word: str):
        matches = re.finditer(REGEX_TYPOS, word)
        if not matches: return [word]
        pos = 0
        res = []
        for match in matches:
            if match.start() > pos: res.append([word[pos:match.start()]])
            value = match.group()
            replace = TYPO_MAPPING.get(value, None)
            if replace is None:
                if match.start() > 0 or match.end() < len(word): replace = [value[0], value]
                else: replace = [value]
            res.append(replace)
            pos = match.end()
        if pos < len(word): res.append([word[pos:]])
        return res

    @staticmethod
    def generate_candidates(word):
        res = [""]
        segments: List = PolishCorrector.get_possible_corrections(word)
        for segment in segments:
            res_copy = res[:]
            res = []
            values = segment if len(res_copy) < 100 else segment[0]
            for value in values:
                res.extend([text + value for text in res_copy])
        return res

    def __correct_typo(self, word):
        candidates = self.generate_candidates(word)
        for candidate in candidates:
            res = self.__find_word(candidate)
            if res is not None: return res
        return None

    def correct(self, word):
        res = self.badword_detector.get_censored_badword(word)
        res = self.__find_word(res)
        if res is not None: return res
        res = self.__correct_typo(word)
        return word if res is None else res

    def correct_text(self, text):
        """
        Correct all the words within a text, returning the corrected text."""
        return re.sub('[^\W\d_]+', self.correct_match, text, flags=re.UNICODE)

    def correct_match(self, match):
        """
        Spell-correct word in match, and preserve proper upper/lower/title case.
        """
        word = match.group()
        return case_of(word)(self.correct(word.lower()))