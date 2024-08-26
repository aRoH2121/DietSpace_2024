from django.core.management.base import BaseCommand
from myapp.models import Utente, Alimento, Dieta, Pasto
import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render

class Command(BaseCommand):
    help = 'Inserisce dati casuali nelle tabelle Alimento, Dieta e Pasto'

    def handle(self, *args, **kwargs):
        def create_random_alimenti(n):
            nomi = ['Mela', 'Banana', 'Carota', 'Broccoli', 'Pollo', 'Salmone', 'Pasta', 'Riso']
            for _ in range(n):
                nome = random.choice(nomi)
                proteine = random.uniform(0, 50)
                grassi = random.uniform(0, 50)
                carboidrati = random.uniform(0, 50)
                calorie = proteine * 4 + grassi * 9 + carboidrati * 4
                Alimento.objects.create(nome=nome, proteine=proteine, grassi=grassi, carboidrati=carboidrati, calorie=calorie)
            self.stdout.write(self.style.SUCCESS('Alimenti creati con successo'))

        def create_random_dieta(paziente, medico, n_diete):
            for _ in range(n_diete):
                nome_dieta = f"Dieta {_ + 1}"
                data_dieta = timezone.now() - timedelta(days=random.randint(0, 365))
                dieta = Dieta.objects.create(id_medico=medico, paziente=paziente, data=data_dieta, nome=nome_dieta)
                create_random_pasti(dieta)
            self.stdout.write(self.style.SUCCESS('Diete create con successo'))

        def create_random_pasti(dieta):
            tipi_pasto = ['C', 'P', 'S']  # C: Colazione, P: Pranzo, S: Cena
            giorni_settimana = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi', 'Sabato', 'Domenica']
            alimenti = list(Alimento.objects.all())
            
            for giorno in giorni_settimana:
                for tipo in tipi_pasto:
                    alimento = random.choice(alimenti)
                    qta = random.uniform(50, 200)
                    Pasto.objects.create(idDieta=dieta, idalimento=alimento, tipo=tipo, giorno=giorno, qta=qta)
            self.stdout.write(self.style.SUCCESS('Pasti creati con successo'))

        # Parametri
        n_alimenti = 5  # Numero di alimenti da creare
        n_diete = 5  # Numero di diete da creare per il paziente
        paziente_id = 4  # ID del paziente (assicurati che esista)
        medico_id = 2  # ID del medico (assicurati che esista)
        
        # Recupera il paziente e il medico
        paziente = get_object_or_404(Utente, id=paziente_id)
        medico = get_object_or_404(Utente, id=medico_id)
        
        # Crea alimenti casuali
        create_random_alimenti(n_alimenti)
        
        # Crea diete casuali per il paziente
        create_random_dieta(paziente, medico, n_diete)
