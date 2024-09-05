from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  *
from .forms import UtenteCreationForm, UtenteChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = UtenteCreationForm
    form = UtenteChangeForm
    model = Utente
    list_display = ['email', 'nome', 'cognome', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('cf', 'nome', 'cognome', 'provincia', 'telefono', 'genere', 'data_nascita', 'foto_profilo', 'tipo_utente')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'cf', 'nome', 'cognome', 'provincia', 'telefono', 'genere', 'data_nascita', 'foto_profilo', 'tipo_utente', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'nome', 'cognome')
    ordering = ('email',)

admin.site.register(Utente, CustomUserAdmin)
admin.site.register(Alimento)
admin.site.register(Dieta)
admin.site.register(Chat)
admin.site.register(Appuntamento)
admin.site.register(Pesata)
admin.site.register(Message)
admin.site.register(Cura)
admin.site.register(Studio)
admin.site.register(Pasto)
