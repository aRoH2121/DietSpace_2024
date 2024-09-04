from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import *

class UtenteModelTestCase(TestCase):
    def setUp(self):
        self.dottore = Utente.objects.create_user(
            username='dottore', email='dottore@example.com', password='password',tipo_utente=True,  # Dottore
            cf='DTTDRT70A01F205Z',nome='Mario',cognome='Rossi',provincia='RM',telefono='3331234567',genere='M',data_nascita='1970-01-01',
            foto_profilo='avatar-dottore.png'
        )

        self.paziente = Utente.objects.create_user(username='paziente', email='paziente@example.com', password='password',tipo_utente=False,#Paziente
            cf='PZNTST80A01F205Z',nome='Luigi',cognome='Bianchi',provincia='MI',telefono='3337654321',genere='M',data_nascita='1980-01-01',
            foto_profilo='avatar-paziente.png'
        )

    def UserCreationTest(self):
        self.assertTrue(self.dottore.tipo_utente)
        self.assertFalse(self.paziente.tipo_utente)

    def CuraCreationTest(self):
        cura = Cura.objects.create(
            idDottore=self.dottore, 
            idPaziente=self.paziente, 
            statoRichiesta=0
        )
        self.assertEqual(cura.idDottore, self.dottore)
        self.assertEqual(cura.idPaziente, self.paziente)

    def InvalidUserTest(self):
        self.paziente.tipo_utente = True
        self.paziente.save()
        with self.assertRaises(ValidationError):
            cura = Cura(idDottore=self.dottore, idPaziente=self.paziente)
            cura.clean()

        self.dottore.tipo_utente = False
        self.dottore.save()
        with self.assertRaises(ValidationError):
            cura = Cura(idDottore=self.dottore, idPaziente=self.paziente)
            cura.clean()


class ChatMessageTestCase(TestCase):
    def setUp(self):
        self.utente1= Utente.objects.create_user(username='dottore', email='dottore@example.com', password='password',tipo_utente=True,  # Dottore
            cf='DTTDRT70A01F205Z',nome='Mario',cognome='Rossi',provincia='RM',telefono='3331234567',genere='M',
            data_nascita='1970-01-01',foto_profilo='avatar-dottore.png'
        )

        self.utente2 = Utente.objects.create_user(username='paziente', email='paziente@example.com', password='password',tipo_utente=False,  # Paziente
            cf='PZNTST80A01F205Z',nome='Luigi',cognome='Bianchi',provincia='MI',telefono='3337654321',genere='M',
            data_nascita='1980-01-01',foto_profilo='avatar-paziente.png'
        )
        self.chat = Chat.objects.create()
        self.chat.participants.set([self.utente1, self.utente2])
    
    def ChatCreationTest(self):
        self.assertIn(self.utente1, self.chat.participants.all())
        self.assertIn(self.utente2, self.chat.participants.all())

    def MessageCreationTest(self):
        messaggio = Message.objects.create(chat=self.chat, sender=self.utente1, content="Ciao!")
        self.assertEqual(messaggio.chat, self.chat)
        self.assertEqual(messaggio.sender, self.utente1)
        self.assertEqual(messaggio.content, "Ciao!")
    
    def MessagevisualizationTest(self):
        messaggio = Message.objects.create(chat=self.chat, sender=self.utente1, content="Ciao!")
        serialized_message = messaggio.serialize()
        self.assertEqual(serialized_message['content'], "Ciao!")
        self.assertEqual(serialized_message['sender']['username'], self.utente1.username)