from django.urls import path
from . import views as views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home/', views.home, name='home'), 
    path('signup/', views.SignUp, name='signup'), 
    path('', views.Login, name='login'), 
    path('logout/',views.Logout,name='logout'),
    path('login/',views.Login,name='login'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('edit_profile/', views.edit_profile, name='edit_profile'), 
    path('edit_studio/', views.edit_studio, name='edit_studio'),

    path('diet/', views.diet, name='diet'),
    path('ricerca_medici/', views.ricerca, name='ricerca'),
    path('pazienti/', views.Pazienti, name='mypats'),
    path('pazienti/<int:idPazienteSel>/', views.infoPaziente, name='info_paziente'),

    path('richiesta_cura/<int:dottore_id>/', views.richiesta_cura, name='richiesta_cura'),
    path('accetta_richiesta/<int:cura_id>/', views.AccettaRichiesta, name='accetta_richiesta'),
    path('rifiuta_richiesta/<int:cura_id>/', views.RifiutaRichiesta, name='rifiuta_richiesta'),

    path('richiesta_appuntamento/<int:idDottore>/', views.crea_appuntamento, name='richiesta_appuntamento'),
    path('accetta_appuntamento/<int:app_id>/', views.accettaAppuntamento, name='accetta_appuntamento'),
    path('rifiuta_rappuntamento/<int:app_id>/', views.rifiutaAppuntamento, name='rifiuta_appuntamento'),
    path('modifica_appuntamento/', views.modifica_appuntamento, name='modifica_appuntamento'),
    path('elimina_appuntamento/<int:app_id>', views.eliminaAppuntamento, name='elimina_appuntamento'),

    path('pazienti/<int:idPazienteSel>/aggiungi_pesata/', views.aggiungi_pesata, name='aggiungi_pesata'),
    path('pazienti/<int:idPazienteSel>/rimuovi_pesata/', views.rimuovi_pesata, name='rimuovi_pesata'),
    path('pazienti/<int:idPazienteSel>/crea_dieta/', views.crea_dieta, name='crea_dieta'),
    path('pazienti/<int:idPazienteSel>/rimuovi_dieta/', views.rimuovi_dieta, name='rimuovi_dieta'),
    
    path('aggiungi_pasto/', views.aggiungi_pasto, name='aggiungi_pasto'),
    path('rimuovi_pasto/', views.rimuovi_pasto, name='rimuovi_pasto'),
   
    path('chats/', views.chats, name='chats'),
    path('messages/<int:chat_id>/', views.chat_details, name='chat_details'),
    path('add_message/', views.add_message, name='add_message'),
    path('profilo/', views.profile, name='profilo'),
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)