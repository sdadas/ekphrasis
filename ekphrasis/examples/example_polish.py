from collections import Counter

from ekphrasis.classes.polish.badwords import BadwordDetector
from ekphrasis.classes.polish.polishcorrect import PolishCorrector
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons
from ekphrasis.utils.helpers import read_stats

polish_unigrams = Counter(read_stats("polish", 1))
text_processor = TextPreProcessor(
    onstart=[BadwordDetector(corpus=polish_unigrams).correct_text],
    normalize=['url', 'email', 'percent', 'money', 'phone', 'user', 'time', 'date', 'number'],
    annotate={"hashtag", "allcaps", "elongated", "repeated", 'emphasis', 'censored'},
    fix_html=True,
    segmenter="polish",
    corrector="polish",
    unpack_hashtags=True,
    unpack_contractions=False,
    spell_correct_elong=False,
    mode="slow",
    tokenizer=SocialTokenizer(lowercase=True).tokenize,
    correction_method=PolishCorrector(corpus=polish_unigrams).correct_text,
    dicts=[emoticons]
)

sentences = [
"Jaki on był fajny xdd pamiętam, że spóźniłam się na jego pierwsze zajęcia i to sporo i za karę kazał mi usiąść w pierwszej ławce XD",
"@anonymized_account No nie ma u nas szczęścia 😉",
"@anonymized_account Dawno kogoś tak wrednego nie widziałam xd",
"@anonymized_account @anonymized_account Zaległości były, ale ważne czy były wezwania do zapłaty z których się klub nie wywiązał.",
"@anonymized_account @anonymized_account @anonymized_account Gdzie jest @anonymized_account . Brudziński jesteś kłamcą i marnym kutasem @anonymized_account",
"@anonymized_account @anonymized_account  no mam nadzieje !!:)",
"@anonymized_account @anonymized_account Może gustował w starszych paniach ;-)",
"swietowac uchwalenie Konstytucji 3 maja i łamać Konstytucję RP obecnie obowiązującą?!\n#3Maja - dzień hipokryzji.",
"Ahnherr der Schtwätzer wykonawcy Von Spar\nhttps://t.co/SOtenSqIr0",
"Jakiś program na TVN, nauka jazdy za kierownicą babcia śpiewa \"jadą jadą jadą świry jadą\" jadą jadą jadą świry jadą\"",
"@anonymized_account to ich wymień.W czym problem ?",
"Dobry dzień na przypomnienie sobie genezy gwiazdek na fladze #UE #deklaracjaRzymska",
"@anonymized_account @anonymized_account @anonymized_account @anonymized_account Wonder!! Chyba cię....😁😁😁😁😁.No dobra. Na jaki?😁😁😁",
"@anonymized_account @anonymized_account No to Skończmy kurwa z tym wersalem w j...ej szczujni",
"RT @anonymized_account @anonymized_account Żal ci biedaku??? Gdyby nie Kaczyński to by je twoi przyjaciele z PO rozkradl",
"@anonymized_account byłem w pracy ale zaraz odpalam meczyk na yt.Dzięki za walke !!!!:)",
"Pierwsze zdanie: \"Paczka papierosów kosztuje 4 miliardy marek\".\n#JajoWęża teraz na @anonymized_account",
"huju jebany oddawaj server gnoju glubi frajezre kutasie oddawaj bo cie zajebie huju zzglosilem cie i tak nie będziesz miec konta hahahahahahahhahahahaahha",
"@anonymized_account no ja właśnie to samoXD znaczy wiem ze Emre wbija często, bo jego żona jest polką ale no",
"daj znać @anonymized_account o  zdjecie blokady",
"Zależy jak na to spojrzeć. Z jednej strony akredytacja, z drugiej wyjazd za swoje $$$ 😉",
"@anonymized_account Polska to nie napis na dropsie, uuuu, niedobrze, uuuuuuu",
"@anonymized_account @anonymized_account pewnie ranking Fifa bedzie decydowal",
"jak Patryk Jaki wygra wybory w Warszawie oczyści stolicę z byłych UBECKICH funkcjonariuszy ! #woronicza17",
"macie jej numer zdissujcie ją 8)",
"Ja mam dla ciebie lepszą propozycję : powieś się gdzieś pod lasem UB-ecka gnido .",
"Gosia się bardzo nudzi i chętnie z wami porozmawia. macie jej numer - [NUMER TEL.] dzwonić może każdy, ale sms tylko plus."
]

for s in sentences:
    print(" ".join(text_processor.pre_process_doc(s)))