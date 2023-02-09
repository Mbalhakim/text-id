import string

from nltk import SnowballStemmer


class TextModel:
    """A class supporting complex models of text."""

    def __init__(self):
        """Create an empty TextModel."""
        #
        # Maak dictionary's voor elke eigenschap
        #
        self.words = {}  # Om woorden te tellen
        self.word_lengths = {}  # Om woordlengtes te tellen
        self.stems = {}  # Om stammen te tellen
        self.sentence_lengths = {}  # Om zinslengtes te tellen
        #
        # Maak een eigen dictionary
        #
        self.my_feature = {}  # Om ... te tellen
        self.text = ""
        self.punctuation = {}  # Om interpunctie te tellen
        self.g_woorden = () # woorden die de letter G bevatten

    def __repr__(self):
        """Toon de inhoud van een TextModel."""
        s = 'Woorden:\n' + str(self.words) + '\n\n'
        s += 'Woordlengtes:\n' + str(self.word_lengths) + '\n\n'
        s += 'Stammen:\n' + str(self.stems) + '\n\n'
        s += 'Zinslengtes:\n' + str(self.sentence_lengths) + '\n\n'
        s += 'Leestekens:\n' + str(self.punctuation) + '\n\n'
        s += 'Woorden met de letter G:\n' + str(self.g_woorden)

        return s

    # Voeg hier andere methodes toe.
    # Je hebt in het bijzonder methodes nodig die het model vullen.

    def read_text_from_file(self, filename):
        """Lees tekst uit een bestand en wijs deze toe aan de `text` attribuut"""
        with open(filename, 'r') as f:
            self.text = f.read()
            return self.text

    def make_sentence_lengths(self):
        """vervangt tekst in zinnen en telt de lengte van elke zin"""
        text = self.text.replace("!", ".").replace("?", ".")  # vervang alle leestekens
        sentences = [sentence.strip() for sentence in text.split(".") if sentence]  # negeer lege ruimtes
        # gebruik list comprehension om zinslengtes te tellen
        self.sentence_lengths = {len(sentence.split()): sentences.count(sentence) for sentence in sentences}

    def make_punctuation(self):
        # gebruik list comprehension om lesstekens te  tellen
        self.punctuation = {punctuation: self.text.count(punctuation) for punctuation in ["!", ".", "?"]}

    def make_g_woorden(self):
        # gebruik list comprehension om woorden met de letter G te  tellen
        self.g_woorden = {g_woorden: self.clean_string(self.text).count(g_woorden) for g_woorden in ["g"]}

    def make_word_lengths(self):
        """Tel de lengte van elk woord in de tekst en sla de resultaten op in een dictionary"""
        words = self.clean_string(self.text).split()
        # Gebruikt list comprehension om woordlengtes tellen
        word_lengths = {word: len(word) for word in words}
        self.word_lengths = word_lengths

    def make_words(self):
        # wordt hier een dictionary gemaakt van de opgeschoonde woorden met behulp van clean_string()
        clean_s = self.clean_string(self.text)
        words = clean_s.split()
        for word in words:
            if word in self.words:
                self.words[word] += 1
            else:
                self.words[word] = 1

    def clean_string(self, s):
        # De methode clean_string(self, s) krijgt een string mee en geeft een opgeschoonde versie ervan terug zonder
        # leestekens en zonder hoofdletters.
        s = s.lower()
        for p in string.punctuation:
            s = s.replace(p, '')
        return s

    def make_stems(self):
        # De methode make_stems(self) maakt een dictionary van de stammen van de woorden, de woorden zijn opgeschoond
        # met clean_string()
        stemmer = SnowballStemmer("dutch")
        cleaned_text = tm.clean_string(tm.text)
        words = cleaned_text.split()
        for word in words:
            stem = stemmer.stem(word)
            if stem in self.stems:
                self.stems[stem] += 1
            else:
                self.stems[stem] = 1


# zorg dat deze tekst in een bestand genaamd test.txt staat
test_text = """Dit is een korte zin. Dit is geen korte zin, omdat
deze zin meer dan 10 woorden en een getal bevat! Dit is
geen vraag, of wel?"""


clean_text = """dit is een korte zin dit is geen korte zin omdat
deze zin meer dan 10 woorden en een getal bevat dit is
geen vraag of wel"""

tm = TextModel()

tm.read_text_from_file('test.txt')

tm.make_sentence_lengths()

tm.make_word_lengths()

tm.make_punctuation()

clean_s = tm.clean_string(tm.text)

tm.make_words()

tm.make_stems()

tm.make_g_woorden()


assert tm.text == test_text

assert tm.sentence_lengths == {16: 1, 5: 1, 6: 1}

assert tm.punctuation == {"!": 1, ".": 1, "?": 1}

assert tm.words == {
    'dit': 3, 'is': 3, 'een': 2, 'korte': 2, 'zin': 3, 'geen': 2,
    'omdat': 1, 'deze': 1, 'meer': 1, 'dan': 1, '10': 1, 'woorden': 1,
    'en': 1, 'getal': 1, 'bevat': 1, 'vraag': 1, 'of': 1, 'wel': 1
}


assert tm.stems == {
    'dit': 3, 'is': 3, 'een': 2, 'kort': 2, 'zin': 3, 'gen': 2,
    'omdat': 1, 'dez': 1, 'mer': 1, 'dan': 1, '10': 1, 'woord': 1,
    'en': 1, 'getal': 1, 'bevat': 1, 'vrag': 1, 'of': 1, 'wel': 1
}

assert clean_s == clean_text


print(clean_s)


print('TextModel:', tm)
