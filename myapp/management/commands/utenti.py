import os
import json
from django.core.management.base import BaseCommand
from myapp.models import Utente
from pathlib import Path

class Command(BaseCommand):
    help = 'Carica i dati degli utenti da un file JSON nel database'

    def handle(self, *args, **kwargs):
        # Percorso al file JSON
        json_file_path = Path('utenti.json')

        if not json_file_path.exists():
            self.stdout.write(self.style.ERROR(f"Il file {json_file_path} non esiste."))
            return

        # Apri il file JSON e carica i dati
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Itera sui dati e crea oggetti Utente
        for item in data:
            Utente.objects.create(
                cf=item['cf'],
                nome=item['nome'],
                cognome=item['cognome'],
                provincia=item['provincia'],
                telefono=item['telefono'],
                email=item['email'],
                genere=item['genere'],
                data_nascita=item['data_nascita'],
                foto_profilo=item['foto_profilo'],
                tipo_utente=item['tipo_utente']
            )

        self.stdout.write(self.style.SUCCESS('Dati caricati con successo nel database'))
