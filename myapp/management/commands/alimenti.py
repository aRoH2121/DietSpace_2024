import random
from django.core.management.base import BaseCommand
from myapp.models import Alimento

class Command(BaseCommand):
    help = 'Popola il database con un elenco esteso di alimenti usati dai nutrizionisti'

    def handle(self, *args, **kwargs):
        alimenti = [
            # Frutta
            {"nome": "Mela", "proteine": 0.3, "grassi": 0.2, "carboidrati": 14.0, "calorie": 52.0, "categoria": "Fru"},
            {"nome": "Banana", "proteine": 1.1, "grassi": 0.3, "carboidrati": 23.0, "calorie": 96.0, "categoria": "Fru"},
            {"nome": "Arancia", "proteine": 0.9, "grassi": 0.1, "carboidrati": 12.0, "calorie": 47.0, "categoria": "Fru"},
            {"nome": "Fragola", "proteine": 0.8, "grassi": 0.3, "carboidrati": 8.0, "calorie": 32.0, "categoria": "Fru"},
            {"nome": "Uva", "proteine": 0.7, "grassi": 0.2, "carboidrati": 18.0, "calorie": 69.0, "categoria": "Fru"},
            {"nome": "Pera", "proteine": 0.4, "grassi": 0.1, "carboidrati": 15.0, "calorie": 57.0, "categoria": "Fru"},
            {"nome": "Pesca", "proteine": 0.9, "grassi": 0.3, "carboidrati": 9.5, "calorie": 39.0, "categoria": "Fru"},
            {"nome": "Ananas", "proteine": 0.5, "grassi": 0.1, "carboidrati": 13.1, "calorie": 50.0, "categoria": "Fru"},
            {"nome": "Mango", "proteine": 0.8, "grassi": 0.4, "carboidrati": 15.0, "calorie": 60.0, "categoria": "Fru"},
            {"nome": "Melone", "proteine": 0.8, "grassi": 0.2, "carboidrati": 8.2, "calorie": 34.0, "categoria": "Fru"},

            # Verdura
            {"nome": "Carota", "proteine": 0.9, "grassi": 0.2, "carboidrati": 10.0, "calorie": 41.0, "categoria": "Ver"},
            {"nome": "Spinaci", "proteine": 2.9, "grassi": 0.4, "carboidrati": 3.6, "calorie": 23.0, "categoria": "Ver"},
            {"nome": "Broccoli", "proteine": 2.8, "grassi": 0.4, "carboidrati": 7.0, "calorie": 34.0, "categoria": "Ver"},
            {"nome": "Peperone rosso", "proteine": 1.0, "grassi": 0.3, "carboidrati": 6.0, "calorie": 31.0, "categoria": "Ver"},
            {"nome": "Zucchine", "proteine": 1.2, "grassi": 0.3, "carboidrati": 3.1, "calorie": 17.0, "categoria": "Ver"},
            {"nome": "Melanzane", "proteine": 1.0, "grassi": 0.2, "carboidrati": 5.9, "calorie": 25.0, "categoria": "Ver"},
            {"nome": "Cavolfiore", "proteine": 1.9, "grassi": 0.3, "carboidrati": 4.3, "calorie": 25.0, "categoria": "Ver"},
            {"nome": "Cavolo", "proteine": 2.5, "grassi": 0.2, "carboidrati": 5.8, "calorie": 31.0, "categoria": "Ver"},
            {"nome": "Cetriolo", "proteine": 0.7, "grassi": 0.1, "carboidrati": 3.6, "calorie": 16.0, "categoria": "Ver"},
            {"nome": "Lattuga", "proteine": 1.4, "grassi": 0.2, "carboidrati": 2.9, "calorie": 15.0, "categoria": "Ver"},
            {"nome": "Zucca", "proteine": 1.0, "grassi": 0.1, "carboidrati": 6.5, "calorie": 26.0, "categoria": "Ver"},
            {"nome": "Asparagi", "proteine": 2.2, "grassi": 0.2, "carboidrati": 3.9, "calorie": 20.0, "categoria": "Ver"},
            {"nome": "Barbabietola", "proteine": 1.6, "grassi": 0.2, "carboidrati": 10.0, "calorie": 43.0, "categoria": "Ver"},

            # Cereali
            {"nome": "Riso bianco", "proteine": 2.7, "grassi": 0.3, "carboidrati": 28.0, "calorie": 130.0, "categoria": "Cer"},
            {"nome": "Quinoa", "proteine": 4.4, "grassi": 1.9, "carboidrati": 21.3, "calorie": 120.0, "categoria": "Cer"},
            {"nome": "Farro", "proteine": 3.7, "grassi": 0.8, "carboidrati": 22.0, "calorie": 119.0, "categoria": "Cer"},
            {"nome": "Avena", "proteine": 2.4, "grassi": 1.4, "carboidrati": 12.0, "calorie": 68.0, "categoria": "Cer"},
            {"nome": "Orzo", "proteine": 2.3, "grassi": 0.4, "carboidrati": 28.2, "calorie": 123.0, "categoria": "Cer"},
            {"nome": "Segale", "proteine": 3.8, "grassi": 1.0, "carboidrati": 22.9, "calorie": 105.0, "categoria": "Cer"},
            {"nome": "Grano saraceno", "proteine": 3.4, "grassi": 1.0, "carboidrati": 19.9, "calorie": 92.0, "categoria": "Cer"},
            {"nome": "Mais", "proteine": 3.3, "grassi": 1.2, "carboidrati": 19.0, "calorie": 86.0, "categoria": "Cer"},

            # Legumi
            {"nome": "Lenticchie", "proteine": 9.0, "grassi": 0.4, "carboidrati": 20.0, "calorie": 116.0, "categoria": "Leg"},
            {"nome": "Fagioli neri", "proteine": 8.9, "grassi": 0.5, "carboidrati": 23.7, "calorie": 132.0, "categoria": "Leg"},
            {"nome": "Fagioli cannellini", "proteine": 7.0, "grassi": 0.5, "carboidrati": 22.0, "calorie": 118.0, "categoria": "Leg"},
            {"nome": "Ceci", "proteine": 8.9, "grassi": 2.6, "carboidrati": 27.4, "calorie": 164.0, "categoria": "Leg"},
            {"nome": "Piselli", "proteine": 5.4, "grassi": 0.4, "carboidrati": 14.5, "calorie": 81.0, "categoria": "Leg"},
            {"nome": "Soia", "proteine": 12.3, "grassi": 6.4, "carboidrati": 30.0, "calorie": 172.0, "categoria": "Leg"},
            {"nome": "Fave", "proteine": 8.0, "grassi": 0.5, "carboidrati": 19.0, "calorie": 88.0, "categoria": "Leg"},
            {"nome": "Lupini", "proteine": 15.6, "grassi": 2.9, "carboidrati": 9.9, "calorie": 119.0, "categoria": "Leg"},
            {"nome": "Cicerchia", "proteine": 12.0, "grassi": 1.3, "carboidrati": 31.0, "calorie": 174.0, "categoria": "Leg"},

            # Carni bianche
            {"nome": "Petto di pollo", "proteine": 31.0, "grassi": 3.6, "carboidrati": 0.0, "calorie": 165.0, "categoria": "Car"},
            {"nome": "Tacchino", "proteine": 29.0, "grassi": 1.5, "carboidrati": 0.0, "calorie": 135.0, "categoria": "Car"},
            {"nome": "Coniglio", "proteine": 20.0, "grassi": 8.0, "carboidrati": 0.0, "calorie": 173.0, "categoria": "Car"},
            {"nome": "Anatra", "proteine": 19.0, "grassi": 28.0, "carboidrati": 0.0, "calorie": 337.0, "categoria": "Car"},
            {"nome": "Quaglia", "proteine": 21.5, "grassi": 10.3, "carboidrati": 0.0, "calorie": 201.0, "categoria": "Car"},
            
            # Carni rosse
            {"nome": "Carne di manzo", "proteine": 26.1, "grassi": 17.0, "carboidrati": 0.0, "calorie": 250.0, "categoria": "Car"},
            {"nome": "Carne di agnello", "proteine": 25.6, "grassi": 20.3, "carboidrati": 0.0, "calorie": 294.0, "categoria": "Car"},
            {"nome": "Prosciutto crudo", "proteine": 25.0, "grassi": 14.8, "carboidrati": 0.0, "calorie": 215.0, "categoria": "Car"},
            {"nome": "Salsiccia", "proteine": 18.5, "grassi": 27.0, "carboidrati": 0.0, "calorie": 305.0, "categoria": "Car"},
            {"nome": "Speck", "proteine": 29.4, "grassi": 22.5, "carboidrati": 0.0, "calorie": 342.0, "categoria": "Car"},
            
            # Pesce
            {"nome": "Salmone", "proteine": 20.4, "grassi": 13.4, "carboidrati": 0.0, "calorie": 208.0, "categoria": "Pes"},
            {"nome": "Tonno", "proteine": 29.9, "grassi": 1.0, "carboidrati": 0.0, "calorie": 130.0, "categoria": "Pes"},
            {"nome": "Merluzzo", "proteine": 17.8, "grassi": 0.7, "carboidrati": 0.0, "calorie": 82.0, "categoria": "Pes"},
            {"nome": "Sardina", "proteine": 20.9, "grassi": 11.5, "carboidrati": 0.0, "calorie": 208.0, "categoria": "Pes"},
            {"nome": "Acciuga", "proteine": 28.9, "grassi": 6.7, "carboidrati": 0.0, "calorie": 210.0, "categoria": "Pes"},
            
            # Latticini
            {"nome": "Latte intero", "proteine": 3.4, "grassi": 3.7, "carboidrati": 5.0, "calorie": 61.0, "categoria": "Lat"},
            {"nome": "Latte scremato", "proteine": 3.4, "grassi": 0.1, "carboidrati": 5.0, "calorie": 35.0, "categoria": "Lat"},
            {"nome": "Formaggio parmigiano", "proteine": 35.8, "grassi": 25.8, "carboidrati": 3.0, "calorie": 431.0, "categoria": "Lat"},
            {"nome": "Yogurt greco", "proteine": 10.0, "grassi": 0.4, "carboidrati": 4.0, "calorie": 59.0, "categoria": "Lat"},
            {"nome": "Mozzarella", "proteine": 18.0, "grassi": 17.0, "carboidrati": 2.2, "calorie": 280.0, "categoria": "Lat"},
            {"nome": "Ricotta", "proteine": 11.3, "grassi": 13.0, "carboidrati": 3.0, "calorie": 174.0, "categoria": "Lat"},
            {"nome": "Gorgonzola", "proteine": 21.0, "grassi": 28.0, "carboidrati": 2.0, "calorie": 353.0, "categoria": "Lat"},
            {"nome": "Burro", "proteine": 0.5, "grassi": 81.0, "carboidrati": 0.1, "calorie": 717.0, "categoria": "Lat"},
            {"nome": "Panna", "proteine": 2.0, "grassi": 35.0, "carboidrati": 3.0, "calorie": 337.0, "categoria": "Lat"},
        ]

        for alimento in alimenti:
            # Converti tutti i valori numerici a una cifra decimale al massimo
            for key in ["proteine", "grassi", "carboidrati", "calorie"]:
                alimento[key] = round(alimento[key], 1)
            
            # Crea e salva l'oggetto Alimento
            Alimento.objects.create(
                nome=alimento["nome"],
                proteine=alimento["proteine"],
                grassi=alimento["grassi"],
                carboidrati=alimento["carboidrati"],
                calorie=alimento["calorie"],
                categoria=alimento["categoria"]
            )

        self.stdout.write(self.style.SUCCESS('Database popolato con successo con un dataset esteso di alimenti!'))
