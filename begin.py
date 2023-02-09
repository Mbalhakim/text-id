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
        self.punctuation_counter = {}  # Om interpunctie te tellen

    def __repr__(self):
        """Toon de inhoud van een TextModel."""
        s = 'Woorden:\n' + str(self.words) + '\n\n'
        s += 'Woordlengtes:\n' + str(self.word_lengths) + '\n\n'
        s += 'Stammen:\n' + str(self.stems) + '\n\n'
        s += 'Zinslengtes:\n' + str(self.sentence_lengths) + '\n\n'
        s += 'Leestekens:\n' + str(self.punctuation_counter)
        return s

    # Voeg hier andere methodes toe.
    # Je hebt in het bijzonder methodes nodig die het model vullen.

    def read_text_from_file(self, filename):
        """Lees tekst uit een bestand en wijs deze toe aan de `text` attribuut"""
        with open(filename, 'r') as f:
            self.text = f.read()
            return self.text

    def make_sentence_lengths(self):
        """Tokenizes text into sentences, and counts the length of each sentence"""
        text = self.text.replace("!", ".").replace("?", ".")  # vervang alle leestekens
        sentences = [sentence.strip() for sentence in text.split(".") if sentence]  # negeer lege ruimtes
        # gebruik list comprehension om zinslengtes te tellen
        self.sentence_lengths = {len(sentence.split()): sentences.count(sentence) for sentence in sentences}

    def make_punctuation_counter(self):
        # gebruik list comprehension om lesstekens te  tellen
        self.punctuation_counter = {punctuation: self.text.count(punctuation) for punctuation in ["!", ".", "?"]}


tm = TextModel()

tm.read_text_from_file('test.txt')
# zorg dat deze tekst in een bestand genaamd test.txt staat
test_text = """Dit is een korte zin. Dit is geen korte zin, omdat
deze zin meer dan 10 woorden en een getal bevat! Dit is
geen vraag, of wel?"""

tm.read_text_from_file('test.txt')
assert tm.text == test_text
tm.make_sentence_lengths()
assert tm.sentence_lengths == {16: 1, 5: 1, 6: 1}
tm.make_punctuation_counter()
assert tm.punctuation_counter == {"!": 1, ".": 1, "?": 1}

print('TextModel:',tm)
