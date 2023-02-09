import math
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
        self.g_woorden = {}  # woorden die beginnen met de letter G bevatten
        self.model_info = {}

    def __repr__(self):
        """De methode __repr__(self) geeft een overzicht terug van alle dictionary’s in het model, zodat je ermee kan
        testen en kan controleren dat ze werken. """

        s = '\nWoorden:\n' + str(self.words) + '\n\n'
        s += 'Woordlengtes:\n' + str(self.word_lengths) + '\n\n'
        s += 'Stammen:\n' + str(self.stems) + '\n\n'
        s += 'Zinslengtes:\n' + str(self.sentence_lengths) + '\n\n'
        # Voeg hier andere methodes toe.
        s += 'Leestekens:\n' + str(self.punctuation) + '\n\n'
        s += 'Woorden die beginnen met de letter G:\n' + str(self.g_woorden)

        return s


    # Je hebt in het bijzonder methodes nodig die het model vullen.

    def read_text_from_file(self, filename):
        """de functie read_text_from_file() moet de inhoud van een opgegeven bestand via een string 'filename'
        inlezen en toewijzen aan de variabele self.text als 1 lange string"""

        with open(filename, 'r') as f:
            self.text = f.read()
            return self.text

    def make_sentence_lengths(self):
        """de methode is bedoeld om de lengte van de zinnen in self.text te berekenen en
        deze op te slaan in de dictionary self.sentence_lengths"""
        text = self.text.replace("!", ".").replace("?", ".")  # vervang alle leestekens door een punt
        sentences = [sentence.strip() for sentence in text.split(".") if sentence]  # verwijderd vervolgens eventuele lege ruimtes met strip() voor elke zin in de lijst, door middel van de list comprehension
        # comprehension om de lengte van elke zin in de sentences lijst te bepalen en te tellen hoe vaak die lengte voorkomt
        self.sentence_lengths = {len(sentence.split()): sentences.count(sentence) for sentence in sentences}



    def make_punctuation(self):
        """ telt het aantal leestekens in de tekst en slaat dit op in self.punctuation."""

        # de for loop telt het aantal voorkomens van leestekens in de string
        for s in self.text:
            if s in string.punctuation:
                if s in self.punctuation:
                    self.punctuation[s] += 1
                else:
                    self.punctuation[s] = 1

    def make_g_woorden(self):

        """telt woorden in tekst die beginnen met "g" en slaat dit op in een dictionary g_woorden"""
        """ in de milestone was dit methode niet correct geschreven. in deze versie gebruik ik forloop en telt aleen de woorden de beginnen met de letter g"""

        # string opschonen
        clean_s = self.clean_string(self.text)
        words_g = clean_s.split()
        for word in words_g:
            if word.startswith('g') and word not in self.g_woorden:
                self.g_woorden[word] = 1
            elif word.startswith('g'):
                self.g_woorden[word] += 1

    def make_word_lengths(self):
        """Tel de lengte van elk woord in de tekst en sla de resultaten op in een dictionary"""

        # string opschonen
        words = self.clean_string(self.text).split()
        #woorden in de tekst opgesplitst en voor elk woord wordt de lengte bepaald
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
        # de methode clean_string krijgt een string mee en geeft een opgeschoonde versie ervan terug zonder
        # leestekens en zonder hoofdletters.
        s = s.lower()
        for p in string.punctuation:
            s = s.replace(p, '')
        return s

    def make_stems(self):
        # De methode make_stems() maakt een dictionary van de stammen van de woorden, de woorden zijn opgeschoond
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

    def normalize_dictionary(self, d):
        """de methode normaliseert een dictionary door het som van alle waardes van de dictionary te berekenen en deze
        waardes vervolgens te delen door de som. Hierdoor wordt de som van alle waardes 1.0 en wordt de
        geretourneerde dictionary genormaliseerd. """
        total = sum(d.values())
        for k in d:
            d[k] /= total
        return d

    def smallest_value(self, nd1, nd2):
        """De methode smallest_value() krijgt twee dictionary’s nd1 en nd2 mee uit het model en geeft de kleinste
        positieve waarde terug die in de dictionary’s samen voorkomt """
        values = []
        for d in [nd1, nd2]:
            for value in d.values():
                if value > 0:
                    #voegt de waarde "value" aan de lijst "values" toe
                    values.append(value)
        return min(values)

    def compare_dictionaries(self, d, nd1, nd2):
        """ vergelijkt twee genormaliseerde dictionaries (nd1 en nd2) met dictionary (d). Het
        berekent het totaal aan logaritmische waarden voor elke key als (k) in de (d) dictionary en vergelijkt
        deze met de waarden in de genormaliseerde dictionaries. Als een key niet voorkomt in één van de
        genormaliseerde dictionaries, dan wordt een epsilon waarde gebruikt.dan worden
        de totale waardes van de vergelijking voor beide genormaliseerde dictionaries geretourneerd als een lijst. """
        nd1 = self.normalize_dictionary(nd1)
        nd2 = self.normalize_dictionary(nd2)
        total1 = 0.0
        total2 = 0.0
        epsilon = self.smallest_value(nd1, nd2) / 2

        for k in d:
            if k in nd1:
                total1 += d[k] * math.log2(nd1[k])
            else:
                total1 += d[k] * math.log2(epsilon)

            if k in nd2:
                total2 += d[k] * math.log2(nd2[k])
            else:
                total2 += d[k] * math.log2(epsilon)

        return [total1, total2]

    def create_all_dictionaries(self):
        """De methode create_all_dictionaries(self) vult alle dictionary’s aan de hand van de string in self.text. """
        self.make_sentence_lengths()
        self.make_word_lengths()
        self.make_words()
        self.make_stems()
        self.make_punctuation()
        self.make_g_woorden()

    def compare_text_with_two_models(self, model1, model2):
        # geef model 1 en model 2 namen om de afdrukresultaten gemakkelijker te bekijken
        model1_name = model1.model_info['name']
        model2_name = model2.model_info['name']

        print("Vergelijkingsresultaten:")
        print("{:<20}{:<20}{:<20}".format(f"naam", f"model1:{model1_name}", f"model2:{model2_name}"))
        print("{:<20}{:<20}{:<20}".format("----", "------", "------"))


        """Dit stuk code initialiseert een List dictionaries en voegt verschillende elementen toe aan de 
        lijst. Het voegt resultaten toe van het vergelijken van verschillende Features van drie 
        objecten (self, model1, model2), zoals words, word_lengths, stems, sentence_lengths, punctuation,
        g_woorden. De resultaten van het vergelijken worden bepaald door het gebruik van de functie 
        compare_dictionaries. """

        # er wordt hier geen gebruik van de methode normalize_dictionary() want die methode is al geroepen binnen de methode compare_dictionaries()

        # dictionaries List maken
        dictionaries = []
        #het voegt resultaten toe van het vergelijken van de Feature words van drie objecten (self, model1, model2)
        dictionaries += [['words'] + self.compare_dictionaries(self.words, model1.words,model2.words)]

        # het voegt resultaten toe van het vergelijken van de Feature word_lengths van drie objecten (self, model1, model2)
        dictionaries += [['word_lengths'] + self.compare_dictionaries(self.word_lengths,model1.word_lengths,model2.word_lengths)]

        # het voegt resultaten toe van het vergelijken van de Feature stems van drie objecten (self, model1, model2)
        dictionaries += [['stems'] + self.compare_dictionaries(self.stems, model1.stems,model2.stems)]

        # het voegt resultaten toe van het vergelijken van de Feature sentence_lengths van drie objecten (self, model1, model2)
        dictionaries += [['sentence_lengths'] + self.compare_dictionaries(self.sentence_lengths, model1.sentence_lengths,model2.sentence_lengths)]

        # het voegt resultaten toe van het vergelijken van de Feature punctuation van drie objecten (self, model1, model2)
        dictionaries += [['punctuation'] + self.compare_dictionaries(self.punctuation,model1.punctuation,model2.punctuation)]

        # het voegt resultaten toe van het vergelijken van de Feature g_worden van drie objecten (self, model1, model2)
        dictionaries += [['g_worden'] + self.compare_dictionaries(self.g_woorden, model1.g_woorden, model2.g_woorden)]

        # ":<15" om de breedte van de kolom op 15 tekens te beperken
        # print(dictionaries)

        #het resultaat van words op 2 decimaal afronden
        print("{:<20}{:<20.2f}{:<20.2f}".format(dictionaries[0][0], round(dictionaries[0][1], 2),
                                                round(dictionaries[0][2]), 2))

        # het resultaat van word_lengths op 2 decimaal afronden
        print("{:<20}{:<20.2f}{:<20.2f}".format(dictionaries[1][0], round(dictionaries[1][1], 2),
                                                round(dictionaries[1][2]), 2))
        # het resultaat van stems op 2 decimaal afronden
        print("{:<20}{:<20.2f}{:<20.2f}".format(dictionaries[2][0], round(dictionaries[2][1], 2),
                                                round(dictionaries[2][2]), 2))
        # het resultaat van sentence_lengths op 2 decimaal afronden
        print("{:<20}{:<20.2f}{:<20.2f}".format(dictionaries[3][0], round(dictionaries[3][1], 2),
                                                round(dictionaries[3][2]), 2))
        # het resultaat van punctuation op 2 decimaal afronden
        print("{:<20}{:<20.2f}{:<20.2f}".format(dictionaries[4][0], round(dictionaries[4][1], 2),
                                                round(dictionaries[4][2]), 2))

        # het resultaat van g_worden op 2 decimaal afronden
        print("{:<20}{:<20.2f}{:<20.2f}".format(dictionaries[5][0], round(dictionaries[5][1], 2),
                                                round(dictionaries[5][2]), 2))
        model1_wins = 0
        model2_wins = 0

        # print("testttttt",dictionaries[0][1])
        # als words van model1 is groter dan words van model2 voeg 1 aan model1_wins else voeg 1 aan model1_wins
        if (dictionaries[0][1] > dictionaries[0][2]):
            model1_wins += 1
        else:
            model2_wins += 1

        # als word_lengths van model1 is groter dan word_lengths van model2 voeg 1 aan model1_wins else voeg 1 aan model1_wins
        if (dictionaries[1][1] > dictionaries[1][2]):
            model1_wins += 1
        else:
            model2_wins += 1

        # als stems van model1 is groter dan stems van model2 voeg 1 aan model1_wins else voeg 1 aan model1_wins
        if (dictionaries[2][1] > dictionaries[2][2]):
            model1_wins += 1
        else:
            model2_wins += 1

        # als sentence_lengths van model1 is groter dan sentence_lengths van model2 voeg 1 aan model1_wins else voeg 1 aan model1_wins
        if (dictionaries[3][1] > dictionaries[3][2]):
            model1_wins += 1
        else:
            model2_wins += 1

        # als punctuation van model1 is groter dan punctuation van model2 voeg 1 aan model1_wins else voeg 1 aan model1_wins
        if (dictionaries[4][1] > dictionaries[4][2]):
            model1_wins += 1
        else:
            model2_wins += 1

        # als g_worden van model1 is groter dan g_worden van model2 voeg 1 aan model1_wins else voeg 1 aan model1_wins
        if (dictionaries[5][1] > dictionaries[5][2]):
            model1_wins += 1
        else:
            model2_wins += 1




        print(f'\n-->  Model 1 {model1_name} wint op {model1_wins} features')
        print(f'-->  Model 2 {model2_name} wint op {model2_wins} features')

        if (model1_wins > model2_wins):
            print(f'\n+++++     Model 1 {model1_name} komt beter overeen!     +++++')
        elif (model1_wins < model2_wins):
            print(f'\n+++++     Model 2 {model2_name} komt beter overeen!     +++++')
        else:
            print(f'\n+++++     Beide modellen {model1_name} en {model2_name} komen even goed overeen!     +++++')

        print("\n")


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

assert tm.punctuation == {'!': 1, '.': 1, '?': 1, ',': 2}

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

d = {'a': 2, 'b': 1, 'c': 1, 'd': 1, 'e': 1}
d1 = {'a': 5, 'b': 1, 'c': 2}
nd1 = tm.normalize_dictionary(d1)
d2 = {'a': 15, 'd': 1}
nd2 = tm.normalize_dictionary(d2)
assert nd1 == {'a': 0.625, 'b': 0.125, 'c': 0.25}
assert nd2 == {'a': 0.9375, 'd': 0.0625}
list_of_log_probs = tm.compare_dictionaries(d, nd1, nd2)

assert list_of_log_probs[0] == -16.356143810225277
assert list_of_log_probs[1] == -19.18621880878296
# print(list_of_log_probs)
# print(nd1, nd2, tm.smallest_value(nd1, nd2))
print('Het model bevat deze dictionary\'s:')

# print('TextModel:', tm)

print(' +++++++++++ Model Shakespeare +++++++++++ ')
tm_shk = TextModel()
tm_shk.read_text_from_file('Shakespeare.txt')
tm_shk.create_all_dictionaries()
tm_shk.model_info = {"name":"Shakespeare"}

# print(tm_shk)

print(' +++++++++++ Model Rowling+++++++++++ ')
tm_rol = TextModel()
tm_rol.read_text_from_file('Rowling.txt')
tm_rol.create_all_dictionaries()
tm_rol.model_info = {"name":"Rowling"}
# print(tm_rol)

print(' +++++++++++ Onbekende tekst over het leven +++++++++++ ')
tm_unknown2 = TextModel()
tm_unknown2.read_text_from_file('unknown2.txt')
tm_unknown2.create_all_dictionaries()
tm_unknown2.model_info = {"name":"Unknown2"}
# print(tm_unknown2)

# print(' +++++++++++ Model 1 +++++++++++ ')
tm1 = TextModel()
tm1.read_text_from_file('train1.txt')
tm1.create_all_dictionaries()  # deze is hierboven gegeven
tm1.model_info = {"name":"train1"}
# print(tm1)

# print(' +++++++++++ Model 2+++++++++++ ')
tm2 = TextModel()
tm2.read_text_from_file('train2.txt')
tm2.create_all_dictionaries()  # deze is hierboven gegeven
tm2.model_info = {"name":"train2"}
# print(tm2)

# print(' +++++++++++ Onbekende tekst +++++++++++ ')
tm_unknown = TextModel()
tm_unknown.read_text_from_file('unknown.txt')
tm_unknown.create_all_dictionaries()  # deze is hierboven gegeven
# print(tm_unknown)

tm_soc = TextModel()
tm_soc.read_text_from_file('Socrates.txt')
tm_soc.create_all_dictionaries()  # deze is hierboven gegeven
tm_soc.model_info = {"name":"Socrates"}
# print(tm1)

# print(' +++++++++++ Model 2+++++++++++ ')
tm_pn = TextModel()
tm_pn.read_text_from_file('Pain.txt')
tm_pn.create_all_dictionaries()  # deze is hierboven gegeven
tm_pn.model_info = {"name":"Pain"}
# print(tm2)

# print(' +++++++++++ Onbekende tekst +++++++++++ ')
tm_unknown3 = TextModel()
tm_unknown3.read_text_from_file('unknown3.txt')
tm_unknown3.create_all_dictionaries()  # deze is hierboven gegeven
# print(tm_unknown)


tm_msi = TextModel()
tm_msi.read_text_from_file('Messi.txt')
tm_msi.create_all_dictionaries()  # deze is hierboven gegeven
tm_msi.model_info = {"name":"Messi"}
# print(tm1)

# print(' +++++++++++ Model 2+++++++++++ ')
tm_cr7 = TextModel()
tm_cr7.read_text_from_file('CristianoRonaldo.txt')
tm_cr7.create_all_dictionaries()  # deze is hierboven gegeven
tm_cr7.model_info = {"name":"CR7"}
# print(tm2)

# print(' +++++++++++ Onbekende tekst +++++++++++ ')
tm_unknown4 = TextModel()
tm_unknown4.read_text_from_file('unknown4.txt')
tm_unknown4.create_all_dictionaries()  # deze is hierboven gegeven
# print(tm_unknown)

#train1 en train2 vergelijken
tm_unknown.compare_text_with_two_models(tm1, tm2)
#Shakespeare en J.K. Rowling vergelijken
tm_unknown2.compare_text_with_two_models(tm_shk, tm_rol)
#Socrates en Pain(Naruto serie) vergelijken
tm_unknown3.compare_text_with_two_models(tm_soc, tm_pn)

#Messi en CristianoRonaldo vergelijken. Zelfs deze code kan geen beslissing maken wie beter is dan de andere lol.
tm_unknown4.compare_text_with_two_models(tm_msi, tm_cr7)


