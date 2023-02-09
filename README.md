# text-id
In dit project Python is gebruikt om een statistisch model van tekst te maken waarmee je een auteur of stijl kan “herkennen”, met een verschillende mate van succes, aan de hand van stukken tekst!
Dit programma is een implementatie van een tekstidentificatie algoritme dat de oorsprong van een tekst probeert vast te stellen door vergelijking met twee referentie modellen. Het programma maakt gebruik van drie objecten, namelijk 'tm_unknown', 'tm_model1' en 'tm_model2', die respectievelijk het te identificeren tekstbestand, het eerste referentiemodel en het tweede referentiemodel vertegenwoordigen.

Er worden functies gebruikt voor het inlezen van de bestanden en het genereren van dictionaries voor de drie modellen, en vervolgens worden de kenmerken van de drie objecten vergeleken door middel van de 'compare_text_with_two_models' functie. Het bevat ook een speciale functie genaamd 'make_g_woorden' die het aantal keren telt dat de letter 'g' in een tekst voorkomt.

De vergelijking van de kenmerken van de drie objecten wordt uitgevoerd door de 'compare_dictionaries' functie die de logaritmische waarden van elke sleutel vergelijkt met behulp van de 'normalize_dictionary' functie.

Het resultaat van de vergelijking wordt afgerond tot twee decimalen en gepresenteerd als een lijst van lijsten met de naam van elke feature en het resultaat ervan. De winnaar wordt bepaald door wie het meeste punten heeft van "model1_wins" of "model2_wins".

De implementatie maakt gebruik van een object-georiënteerde aanpak en is geschreven in Python.



