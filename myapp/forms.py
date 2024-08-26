import datetime
from django import forms
from .models import Utente, Dieta, Pasto, Appuntamento, Studio
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth import authenticate, get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utente  # Assicurati che il modello Utente sia importato correttamente
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class UtenteCreationForm(UserCreationForm):
    # Campo data_nascita con widget di tipo date per il selettore di data
    data_nascita = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Data di nascita'
    )
    
    # Campo tipo_utente con radio buttons per selezionare tra Dottore e Paziente
    tipo_utente = forms.ChoiceField(
        choices=[(True, 'Dottore'), (False, 'Paziente')],
        widget=forms.RadioSelect,
        label='Tipologia di account'
    )
    password1 = forms.CharField(
         widget=forms.PasswordInput(attrs={'placeholder': 'Inserisci la tua password'}),
        label='Password', 
        help_text=(  '<p>La password deve rispettare i seguenti requisiti:<p>'
                '<ul>'
                '<li>Deve contenere almeno 8 caratteri.</li>'
                '<li>Non deve essere simile al tuo nome utente o altre informazioni personali.</li>'
                '<li>Non deve essere una password comune.</li>'
                '<li>Non deve essere composta solo da numeri.</li>'
                '</ul>')
     
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Conferma Password'}),
        label='Conferma Password',
        
    )


    class Meta:
        model = Utente
        fields = (
            'username', 'password1', 'password2', 'nome', 'cognome','cf',
            'genere', 'data_nascita', 'tipo_utente', 'telefono', 'email'
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

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get('email')
        data=cleaned_data.get('data_nascita')
        
        # Verifica che le password corrispondano
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Le password non corrispondono")

        try:
            validate_email(email)
        except ValidationError:
            self.add_error('email', "La e-mail inserita non è valida.")
        
        if data > datetime.date.today():
            self.add_error('data_nascita', "Sei nato nel futuro? Inserisci una data valida.")


        # Validatore per il codice fiscale
        cf=cleaned_data.get('cf')
        if len(cf) != 16:
            self.add_error('cf', 'Il codice fiscale deve essere lungo 16 caratteri.')
        if not cf.isalnum():
            self.add_error('cf', 'Il codice fiscale deve contenere solo caratteri alfanumerici.')

        telefono=cleaned_data.get('telefono')
        if len(telefono) != 10 or not telefono.isdigit():
            self.add_error('cf', 'Il numero di telefono deve essere lungo 10 cifre e contenere solo numeri.')


        return cleaned_data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('signup', 'Registrati'))
        
        # Aggiungi log per debugging

class UtenteChangeForm(UserChangeForm):
    class Meta:
        model = Utente
        fields = ('username', 'password', 'cf', 'nome', 'cognome', 'provincia', 'telefono', 'email', 'genere', 'data_nascita', 'foto_profilo', 'tipo_utente', 'is_active', 'is_staff', 'is_superuser')

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
        fields = ['telefono', 'email', 'tipo_utente', 'foto_profilo']  # Includi i campi che vuoi che l'utente possa modificare

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # Imposta i campi 'telefono' e 'email' come obbligatori
        self.fields['telefono'].required = True
        self.fields['email'].required = True
  

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



class StudioForm(forms.ModelForm):
    class Meta:
        model = Studio
        fields = ['via', 'civico', 'citta', 'provincia']

    def __init__(self, *args, **kwargs):
        super(StudioForm, self).__init__(*args, **kwargs)
        # Imposta i campi come obbligatori
        self.fields['via'].required = True
        self.fields['civico'].required = True
        self.fields['citta'].required = True
        self.fields['provincia'].required = True