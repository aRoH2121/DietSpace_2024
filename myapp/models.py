from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError 


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Ensure required fields for superuser creation
        extra_fields.setdefault('data_nascita', '2000-01-01')  # Default value if not provided
        extra_fields.setdefault('cf', '')
        extra_fields.setdefault('nome', '')
        extra_fields.setdefault('cognome', '')
        extra_fields.setdefault('provincia', '')
        extra_fields.setdefault('telefono', '0000000000')
        extra_fields.setdefault('genere', 'M')
        extra_fields.setdefault('foto_profilo', 'avatar-default.png')
        extra_fields.setdefault('tipo_utente', False)

        return self.create_user(username, email, password, **extra_fields)

    def __str__(self):
        return self.username

class Utente(AbstractUser):
    cf = models.CharField(max_length=16, blank=True)
    nome = models.CharField(max_length=30, blank=True)
    cognome = models.CharField(max_length=30, blank=True)
    provincia = models.CharField(max_length=2, blank=True)
    telefono = models.CharField(max_length=10)
    email = models.EmailField(max_length=100, blank=True)
    genere = models.CharField(max_length=1, choices=[('M', 'Maschio'), ('F', 'Femmina')])
    data_nascita = models.DateField()
    foto_profilo = models.ImageField(upload_to='images/', default='images/default.jpg')
    tipo_utente = models.BooleanField(default=False)  # tipo = 1 => dottore, tipo = 0 => paziente

    objects = CustomUserManager()

class Pesata(models.Model):
    idPaziente = models.ForeignKey(Utente, on_delete=models.CASCADE, null=True, related_name='pesata_paziente')
    idDottore=models.ForeignKey(Utente, on_delete=models.CASCADE, null=True,  related_name='pesata_dottore')
    Peso = models.FloatField(default=None,blank=True)
    DataInserimentoPeso = models.DateField()

#utilizzato come per il follow
class Cura(models.Model):
    idDottore = models.ForeignKey(Utente, related_name='cure_dottore', null=True, on_delete=models.CASCADE)
    idPaziente = models.ForeignKey(Utente, related_name='cure_paziente', null=True, on_delete=models.CASCADE)
    statoRichiesta=models.IntegerField(default=-1)

    def clean(self):
        if self.idDottore.tipo_utente is not True:
            raise ValidationError('idDottore deve essere un utente di tipo dottore.')
        if self.idPaziente.tipo_utente is not False:
            raise ValidationError('idPaziente deve essere un utente di tipo paziente.')

        # Verifica se esiste già una richiesta di cura tra questo paziente e dottore
        if Cura.objects.filter(idDottore=self.idDottore, idPaziente=self.idPaziente).exists():
            raise ValidationError('Esiste già una richiesta di cura per questo dottore da parte di questo paziente.')

class Alimento(models.Model):
    nome = models.CharField(max_length=30,blank=True)
    proteine = models.FloatField(default=0,blank=True)
    grassi = models.FloatField(default=0,blank=True)
    carboidrati = models.FloatField(default=0,blank=True)
    calorie = models.FloatField(default=0,blank=True)
    categoria= models.CharField(max_length=3, blank=True)    # Fru -> frutta, Ver -> Verdura, Car -> Carne, Pes -> Pesce, Lat -> Latticini, Cer -> Cereali

class Dieta(models.Model):
    id_medico = models.ForeignKey(Utente, null=True, on_delete=models.CASCADE, related_name='IDMedico')
    paziente = models.ForeignKey(Utente, null=True, on_delete=models.CASCADE, related_name='IDPaziente')
    data = models.DateTimeField()
    nome = models.CharField(max_length=30, blank=True)

class Pasto(models.Model):
    idDieta = models.ForeignKey(Dieta, null=False, on_delete=models.CASCADE)
    idalimento = models.ForeignKey(Alimento, null=False, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1,blank=True)
    giorno = models.CharField(max_length=9,blank=True)
    qta = models.FloatField(default=None,blank=True)

#da mostrare nel profilo del medico
class Studio(models.Model):
    medico = models.OneToOneField(Utente, on_delete=models.CASCADE, limit_choices_to={'tipo_utente': True})
    via = models.CharField(max_length=50,blank=True)
    civico = models.IntegerField(blank=True)
    citta = models.CharField(max_length=30,blank=True)
    provincia = models.CharField(max_length=2,blank=True)
    
class Appuntamento(models.Model):
    Dottore = models.ForeignKey(Utente, related_name='dott_app', null=True, on_delete=models.CASCADE)
    Paziente = models.ForeignKey(Utente, related_name='paz_app', null=True, on_delete=models.CASCADE)
    stato=models.IntegerField(default=0)
    data_ora=models.DateTimeField()

    def clean(self):
        if self.Dottore.tipo_utente is not True:
            raise ValidationError('idDottore deve essere un utente di tipo dottore.')
        if self.Paziente.tipo_utente is not False:
            raise ValidationError('idPaziente deve essere un utente di tipo paziente.')

        # Verifica se esiste già una richiesta di cura tra questo paziente e dottore
        if Cura.objects.filter(idDottore=self.idDottore, idPaziente=self.idPaziente).exists():
            raise ValidationError('Esiste già una richiesta di appuntamento per questo dottore da parte di questo paziente.')
    
class Chat(models.Model):
    participants = models.ManyToManyField(Utente, related_name='chats')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat ID: {self.id}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message ID: {self.id} | Chat ID: {self.chat.id} | Sender: {self.sender.username}"

    def serialize(self):
        return {
            'id': self.id,
            'chat_id': self.chat.id,
            'sender': {
                'id': self.sender.id,
                'username': self.sender.username,
            },
            'content': self.content,
            'timestamp': self.timestamp.strftime("%d %b %Y, %I:%M %p")
        }