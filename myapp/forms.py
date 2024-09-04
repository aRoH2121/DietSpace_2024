import datetime
from django import forms
from .models import Utente, Dieta, Pasto, Appuntamento, Studio
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth import authenticate, get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
import re

import datetime
import re
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm
from .models import Utente  

class UtenteCreationForm(UserCreationForm):
    data_nascita = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Data di nascita'
    )
    
    tipo_utente = forms.ChoiceField(
        choices=[(True, 'Dottore'), (False, 'Paziente')],
        widget=forms.RadioSelect,
        label='Tipologia di account'
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Inserisci la tua password'}),
        label='Password', 
        help_text=(
            '<p>La password deve rispettare i seguenti requisiti:<p>'
            '<ul>'
            '<li>Deve contenere almeno 8 caratteri.</li>'
            '<li>Deve contenere almeno una lettera maiuscola.</li>'
            '<li>Deve contenere almeno una lettera minuscola.</li>'
            '<li>Deve contenere almeno un numero.</li>'
            '<li>Deve contenere almeno un carattere speciale.</li>'
            '<li>Non deve essere simile al tuo nome utente o altre informazioni personali.</li>'
            '</ul>'
        )
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Conferma Password'}),
        label='Conferma Password',
    )

    class Meta:
        model = Utente
        fields = (
            'tipo_utente', 'username', 'email', 'password1', 
            'password2', 'nome', 'cognome', 'cf',
            'genere', 'data_nascita', 'telefono'
        )
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Inserisci il tuo username'}),
            'cf': forms.TextInput(attrs={'placeholder': 'Inserisci il tuo codice fiscale'}),
            'nome': forms.TextInput(attrs={'placeholder': 'Inserisci il tuo nome'}),
            'cognome': forms.TextInput(attrs={'placeholder': 'Inserisci il tuo cognome'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Inserisci il tuo numero di telefono'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Inserisci il tuo indirizzo email'}),
            'genere': forms.Select(attrs={'placeholder': 'Seleziona il tuo genere'})
        }
        labels = {
            'username': 'Nome utente',
            'cf': 'Codice Fiscale',
            'nome': 'Nome',
            'cognome': 'Cognome',
            'telefono': 'Telefono',
            'email': 'Email',
            'genere': 'Sesso',
            'data_nascita': 'Data di nascita',
            'tipo_utente': 'Tipologia di account'
        }
        help_texts = {
            'username': 'Massimo 150 caratteri. Sono ammessi solo lettere, cifre e @/./+/-/_',
            
        }
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Utente.objects.filter(username=username).exists():
            raise forms.ValidationError("Questo nome utente non è disponibile. Scegline un altro.")
        return username

    def clean_data_nascita(self):
        data = self.cleaned_data.get('data_nascita')
        if data > datetime.date.today():
            raise forms.ValidationError("Sei nato nel futuro? Inserisci una data valida.")
        return data

    def clean_cf(self):
        cf = self.cleaned_data.get('cf')
        if len(cf) != 16:
            raise forms.ValidationError('Il codice fiscale deve essere lungo 16 caratteri.')
        if not cf.isalnum():
            raise forms.ValidationError('Il codice fiscale deve contenere solo caratteri alfanumerici.')
        return cf

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if len(telefono) != 10 or not telefono.isdigit():
            raise forms.ValidationError('Il numero di telefono deve essere lungo 10 cifre e contenere solo numeri.')
        return telefono
        
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            self.add_error('email', "La e-mail inserita non è valida.")
      
        if Utente.objects.filter(email=email).exists():
             raise forms.ValidationError("Questa email è già associata ad un account.")
        return email
        

    error_messages = {
        'password_too_similar': _("La password è troppo simile al nome utente."),
        'password_mismatch': _("Le password non corrispondono."),
        'password_criteria': _("Verifica che la tua password rispetti i requisiti."),
    }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        username = cleaned_data.get("username")

        if not password1 or not password2:
            raise forms.ValidationError(_("Entrambe le password sono richieste."))

        if password1 != password2:
            self.add_error('password2', self.error_messages['password_mismatch'])

        if username and password1 and username.lower() in password1.lower():
            self.add_error('password1', self.error_messages['password_too_similar'])
            self.add_error('password2', '')
            
        try:
            validate_password(password1)
        except ValidationError as e:
            self.add_error('password1', self.error_messages['password_criteria'])
            self.add_error('password2', '')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('signup', 'Registrati'))


class UtenteChangeForm(UserChangeForm):
    class Meta:
        model = Utente
        fields = ('username', 'password', 'cf', 'nome', 'cognome', 'provincia', 'telefono', 'email', 
                  'genere', 'data_nascita', 'foto_profilo', 'tipo_utente', 'is_active', 'is_staff', 'is_superuser')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        User = get_user_model()

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                # Se l'autenticazione fallisce, personalizziamo il messaggio di errore
                if not User.objects.filter(username=username).exists():
                    raise forms.ValidationError("L'username inserito non è associato a nessun account.")
                else:
                    raise forms.ValidationError("La password inserita è errata.")
        
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('login', 'Login'))
        

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Utente
        fields = ['nome', 'cognome', 'data_nascita', 'cf', 'genere', 'telefono', 'email', 'foto_profilo']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Valida l'email
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("La e-mail inserita non è valida.")
        
        if Utente.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Questa email è già associata ad un account.")
        
        return email

    def clean_data_nascita(self):
        data = self.cleaned_data.get('data_nascita')
        if data > datetime.date.today():
            raise forms.ValidationError("Sei nato nel futuro? Inserisci una data valida.")
        return data

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        
        # Verifica la lunghezza e il formato del numero di telefono
        if len(telefono) != 10 or not telefono.isdigit():
            raise forms.ValidationError('Il numero di telefono deve essere lungo 10 cifre e contenere solo numeri.')
        
        return telefono

    def clean_cf(self):
        cf = self.cleaned_data.get('cf')
        if len(cf) != 16:
            raise forms.ValidationError('Il codice fiscale deve essere lungo 16 caratteri.')
        if not cf.isalnum():
            raise forms.ValidationError('Il codice fiscale deve contenere solo caratteri alfanumerici.')
        return cf

    def clean(self):
        cleaned_data = super().clean()  # Chiama il metodo di pulizia della classe base
        # Aggiungi ulteriori validazioni a livello di modulo se necessario
        return cleaned_data


  

class DietaForm(forms.ModelForm):
    class Meta:
        model = Dieta
        fields = ['nome', 'data']



class AppuntamentoForm(forms.ModelForm):
    class Meta:
        model = Appuntamento
        fields = ['Dottore', 'Paziente', 'data_ora']
        widgets = {
            'data_ora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        def clean(self):
                cleaned_data = super().clean()
                data_ora = cleaned_data.get('data_ora')

                if data_ora < datetime.datetime.today():
                        raise forms.ValidationError("Indica una data futura! Non è un viaggio nel tempo.")

                return cleaned_data



class StudioForm(forms.ModelForm):
    class Meta:
        model = Studio
        fields = ['via', 'civico', 'citta', 'provincia']

    def __init__(self, *args, **kwargs):
        super(StudioForm, self).__init__(*args, **kwargs)
        self.fields['via'].required = True
        self.fields['civico'].required = True
        self.fields['citta'].required = True
        self.fields['provincia'].required = True


class PasswordResetForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    phone_number = forms.CharField(label='Cellulare', max_length=15)
    new_password = forms.CharField(label='Nuova Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        phone_number = cleaned_data.get('phone_number')

      
        try:
            user = Utente.objects.get(username=username, telefono=phone_number)
        except Utente.DoesNotExist:
            raise forms.ValidationError('Nome utente o numero di cellulare non corrispondono')

        
        return cleaned_data