import os
import re
from collections import Counter
from typing import Set, Dict

from ekphrasis.utils.helpers import read_stats, case_of

CENSORED = re.compile(r'\b[^\W\d_]+[*.]+[^\W\d_]+\b', re.UNICODE)

class BadwordDetector:

    def __init__(self, corpus="polish"):
        source = os.path.join(os.path.dirname(os.path.abspath(__file__)), "badwords.txt")
        self.frequencies = corpus if isinstance(corpus, Counter) else Counter(read_stats(corpus, 1))
        self.badwords: Set[str] = set([line.strip() for line in open(source, "r", encoding="utf-8").readlines()])
        self.censored: Dict[str, str] = self.__build_censored()

    def __build_censored(self):
        res = {}
        for word in self.badwords: self.__build_censored_word(word, res)
        return res

    def __build_censored_word(self, word: str, res: Dict[str, str]):
        if len(word) < 3: return
        for i in range(1, len(word)):
            for j in range(i + 1, len(word)):
                censored = word[:i] + "-" + word[j:]
                if censored not in res or self.frequencies.get(word, 0) > self.frequencies.get(res[censored], 0):
                    res[censored] = word

    def is_bad_word(self, word: str) -> bool:
        return word.lower() in self.badwords

    def get_censored_badword(self, word: str):
        lower = word.lower()
        if lower in self.badwords: return lower
        if re.match(CENSORED, lower):
            val = re.sub(r'[*.]+', "-", lower)
            return self.censored.get(val, word)
        return word

    def correct_text(self, text):
        return re.sub('[^\W\d_]+[*.]+[^\W\d_]+', self.correct_match, text, flags=re.UNICODE)

    def correct_match(self, match):
        word = match.group()
        return case_of(word)(self.get_censored_badword(word.lower()))
