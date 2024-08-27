from datetime import datetime, timedelta, timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from .models import *
from django.core.exceptions import ValidationError 
from django.shortcuts import get_object_or_404, redirect, render
import json
from django.utils.dateparse import parse_datetime
from collections import defaultdict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q
from calendar import monthrange
from django.utils import timezone
ID_DIETA = 0

@login_required
def home(request):
    # Ottieni il contesto dalla funzione graph_data
    context = graph_data(request, request.user.id)
    
    # Ottieni il contesto dalla funzione calendario
    calendario_context = calendario(request)
    
    # Unisci i due contesti
    context.update(calendario_context)
    
    user = request.user
    context['user'] = user
    context['form'] = EditProfileForm(instance=user)  # Form di modifica del profilo
    
    # Ottieni la data e ora corrente
    today = timezone.now()

    if user.tipo_utente:  # Se l'utente è un dottore
        
        try:
            studio = Studio.objects.get(medico=request.user)
            studio_form = StudioForm(instance=studio)  # Form con i dati dello studio esistente
        except Studio.DoesNotExist:
            studio = None
            studio_form = StudioForm()  # Form vuota per creare un nuovo studio

        context['studio'] = studio
        context['studioform'] = studio_form  # Form di modifica dello studio

        # Query per ottenere le richieste di cura pendenti
        cura = Cura.objects.filter(idDottore=user.id, statoRichiesta=2)
        pending = Utente.objects.filter(id__in=cura.values_list("idPaziente", flat=True))
        context['reqPending'] = [{'utente': utente, 'cura_id': cura_obj.id} for utente, cura_obj in zip(pending, cura)]

        # Filtra gli appuntamenti con data >= oggi
        appuntamenti = Appuntamento.objects.filter(Dottore=user.id, data_ora__gte=today).select_related('Paziente')
        
        pazienti = Utente.objects.filter(id__in=appuntamenti.values_list("Paziente_id", flat=True))
        appointments_by_patient = defaultdict(list)
        for appuntamento in appuntamenti:
            appointments_by_patient[appuntamento.Paziente_id].append(appuntamento)

        # Organizza gli appuntamenti per paziente
        appointmentRequests = [{'utente': paziente, 'appuntamenti': appointments_by_patient[paziente.id]} for paziente in pazienti]
        context['appointmentRequests'] = appointmentRequests

    else:
        # Paziente che vede le richieste dei dottori
        cura = Cura.objects.filter(idPaziente=user.id, statoRichiesta=2)
        pending = Utente.objects.filter(id__in=cura.values_list("idDottore", flat=True))
        context['reqPending'] = [{'utente': utente, 'cura_id': cura_obj.id} for utente, cura_obj in zip(pending, cura)]

        # Filtra gli appuntamenti con data >= oggi
        appuntamenti = Appuntamento.objects.filter(Paziente_id=user.id, data_ora__gte=today)
        dottori = Utente.objects.filter(id__in=appuntamenti.values_list("Dottore_id", flat=True))
        appointments_by_doctors = defaultdict(list)
        for appuntamento in appuntamenti:
            appointments_by_doctors[appuntamento.Dottore_id].append(appuntamento)
        
        appointmentRequests = [{'utente': dottore, 'appuntamenti': appointments_by_doctors[dottore.id]} for dottore in dottori]
        context['appointmentRequests'] = appointmentRequests
       
    return render(request, 'home.html', context)

def profile(request):
    
    user = request.user
    context={
        'user' : request.user, 
        'form':   EditProfileForm(instance=user)   
    }
    if user.tipo_utente:
        try:
                studio = Studio.objects.get(medico=request.user)
                studio_form = StudioForm(instance=studio)  # Form con i dati dello studio esistente
        except Studio.DoesNotExist:
                studio = None
                studio_form = StudioForm()  # Form vuota per creare un nuovo studio


        context['studio'] = studio
        context['studioform'] = studio_form  # Form di modifica dello studio

    return render(request, 'profile.html', context)


def SignUp(request):
    if request.method == "POST":
        form = UtenteCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('/login')
            else:
                print('errore nella registrazione')
                messages.warning(request,"I dati inseriti non sono corretti")
                return redirect('/signup')
        else:
            print("Form non valido")
            print(form.errors)
    else:
        form = UtenteCreationForm()

    return render(request, 'auth/signup.html', {'form': form})

def Login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, "Password e/o email non valida")
                return redirect('login')
        else:
            messages.error(request, "Errore nei dati inseriti")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})

def Logout(request):
    logout(request)
    return redirect('login')

login_required
def graph_data(request, idUtente):
    pesi = Pesata.objects.filter(idPaziente=idUtente).order_by('DataInserimentoPeso')
    date_pesi = [peso.DataInserimentoPeso.strftime('%Y-%m-%d') for peso in pesi]
    valori_pesi = [peso.Peso for peso in pesi]

    context = {
        'date_pesi': json.dumps(date_pesi),
        'valori_pesi': json.dumps(valori_pesi),
    }
    return context

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')  # Modifica l'URL di destinazione dopo il salvataggio
    else:
        form = EditProfileForm(instance=request.user)
    return redirect('home')

@login_required
def diet(request):

    paz=get_object_or_404(Utente, id=request.user.id)
    diete = Dieta.objects.filter(paziente=paz).order_by('-data')

    diete_info = []
    for dieta in diete:
            pasti = Pasto.objects.filter(idDieta=dieta)
            pasti_info = []
            for pasto in pasti:
                alimento = get_object_or_404(Alimento, pk=pasto.idalimento_id)
                pasti_info.append({
                    'id': pasto.id,
                    'nome_alimento': alimento.nome,
                    'proteine': alimento.proteine,
                    'grassi': alimento.grassi,
                    'carboidrati': alimento.carboidrati,
                    'calorie': alimento.calorie,
                    'quantita': pasto.qta,
                    'tipo': pasto.tipo,
                    'giorno': pasto.giorno,
                })
            diete_info.append({
                'id': dieta.id,
                'nome': dieta.nome,
                'data': dieta.data,
                'pasti': pasti_info
            })

    context = {
        'diete' : diete_info
    }
    print(context)
    return render(request, 'diet/diet.html', context)

@login_required
def chat(request):
    return render(request, 'chat.html')

@login_required
def ricerca(request):
    paziente = request.user
    doctors = Utente.objects.filter(tipo_utente=True).select_related('studio').order_by('nome', 'cognome')

    # Ottieni le richieste già fatte dal paziente
    richieste_paziente = Cura.objects.filter(idPaziente=paziente).values_list('idDottore_id', flat=True)

    # Ottieni i medici curanti (con statoRichiesta = 1)
    medici_curanti = Cura.objects.filter(idPaziente=paziente, statoRichiesta=1).select_related('idDottore')
    context={
        'doctors': doctors,
        'richieste_dottori': richieste_paziente,
        'medici_curanti': medici_curanti
    }
    return render(request, 'ricerca_medici.html', context)




@login_required
def richiesta_cura(request, dottore_id):
    if request.method == 'POST':
        paziente = request.user
        dottore = get_object_or_404(Utente, id=dottore_id, tipo_utente=True)
        stato = 2  # Pending

        if not paziente.tipo_utente and dottore.tipo_utente:
            try:
                cura = Cura(idDottore=dottore, idPaziente=paziente, statoRichiesta=stato)
                cura.clean()  # Ensure the validation logic is applied
                cura.save()
                messages.success(request, 'Richiesta di cura inviata con successo.')
                return redirect('ricerca')  # Redirect to the search page or another appropriate page
            except ValidationError as e:
                messages.error(request, 'Errore nella richiesta di cura: ' + ' '.join(e.messages))
                # Passa i dati necessari per il rendering della pagina
                doctors = Utente.objects.filter(tipo_utente=True).select_related('studio')
                return render(request, 'ricerca_medici.html', {'doctors': doctors})
        else:
            messages.error(request, 'L\'utente non è un paziente o il dottore non è valido.')
            return redirect('ricerca')

    return redirect('ricerca')

@login_required(login_url='login')
def AccettaRichiesta(request, cura_id):
    cura = get_object_or_404(Cura, id=cura_id)
    cura.statoRichiesta = 1  
    cura.save()
    crea_chat(cura)
    return redirect('home')


def crea_chat(cura):
    medico = cura.idDottore
    paziente = cura.idPaziente

    # Cerca una chat esistente che abbia esattamente questi partecipanti
    existing_chat = Chat.objects.filter(
        participants=medico
    ).filter(
        participants=paziente
    ).distinct().first()

    if not existing_chat:
        # Se non esiste, crea una nuova chat
        chat = Chat.objects.create()
        chat.participants.add(medico, paziente)
        chat.save()
        return chat

    return existing_chat


@login_required(login_url='login')
def RifiutaRichiesta(request, cura_id):
    cura = get_object_or_404(Cura, id=cura_id)
    chat = Chat.objects.filter(participants=cura.idPaziente).filter(participants=cura.idDottore).first()
    if chat:
        print("cancellando")
        chat.delete()
    cura.delete()
    return redirect('home')


@login_required
def Pazienti(request):
    cura = Cura.objects.filter(idDottore=request.user.id, statoRichiesta=1)
    seguiti = Utente.objects.filter(id__in=cura.values_list("idPaziente", flat=True))
    context={'pazienti_seguiti' : [{'utente': utente, 'cura_id': cura_obj.id} for utente, cura_obj in zip(seguiti, cura)]}
    print(context)
    return render(request, 'pats/mypats.html', context)

@login_required
def infoPaziente(request, idPazienteSel):
    pesate=Pesata.objects.filter(idPaziente_id=idPazienteSel).order_by("DataInserimentoPeso")
    paz=get_object_or_404(Utente, id=idPazienteSel)
    diete = Dieta.objects.filter(paziente=paz).order_by('-data')
    alimenti=Alimento.objects.all

    diete_info = []
    for dieta in diete:
            pasti = Pasto.objects.filter(idDieta=dieta)
            pasti_info = []
            for pasto in pasti:
                alimento = get_object_or_404(Alimento, pk=pasto.idalimento_id)
                pasti_info.append({
                    'id': pasto.id,
                    'nome_alimento': alimento.nome,
                    'proteine': alimento.proteine,
                    'grassi': alimento.grassi,
                    'carboidrati': alimento.carboidrati,
                    'calorie': alimento.calorie,
                    'quantita': pasto.qta,
                    'tipo': pasto.tipo,
                    'giorno': pasto.giorno,
                })
            diete_info.append({
                'id': dieta.id,
                'nome': dieta.nome,
                'data': dieta.data,
                'pasti': pasti_info
            })

    context=graph_data(request, idPazienteSel)
    print(context)
    context_info = {
        'pesate' : pesate,
        'paziente' : paz,
        'diete' : diete_info, 
        'alimenti' : alimenti
    }
    context.update(context_info)
    return render(request, 'pats/infopats.html', context)

def aggiungi_pesata(request, idPazienteSel):
    if request.method == 'POST':
        peso = request.POST['peso']
        data = request.POST['data']
        Pesata.objects.create(idPaziente_id=idPazienteSel, Peso=peso, DataInserimentoPeso=data)
        return redirect('info_paziente',idPazienteSel)

def rimuovi_pesata(request, idPazienteSel):
    if request.method == 'POST':
        pesata_id = request.POST['pesata']
        print(pesata_id)
        pesata = get_object_or_404(Pesata, id=pesata_id)
        pesata.delete()
        return redirect('info_paziente', idPazienteSel)


def crea_dieta(request, idPazienteSel):
    if request.method == 'POST':
        dieta_form = DietaForm(request.POST)
        if dieta_form.is_valid():
            dieta = dieta_form.save(commit=False)
            dieta.id_medico = request.user  # Imposta il medico che crea la dieta
            dieta.paziente= get_object_or_404(Utente, id=idPazienteSel)  # Imposta il medico che crea la dieta
            dieta.save()
    else:
        dieta_form = DietaForm()
    return redirect('info_paziente', idPazienteSel)   


def rimuovi_dieta(request, idPazienteSel):
    if request.method == 'POST':
        dieta_id = request.POST.get('dieta_id')  
        dieta = get_object_or_404(Dieta, id=dieta_id, paziente_id=idPazienteSel)
        
        if dieta.id_medico == request.user:
            dieta.delete() 
        
    return redirect('info_paziente', idPazienteSel)



def aggiungi_pasto(request):
    print('Aggiunta pasto view')
    if request.method == 'POST':
        dietaID=request.POST['dietaID']
        tipo = request.POST['tipo']
        giorno_ = request.POST['giorno']
        alimento = request.POST['alimento']
        qta = request.POST['qta']
        dieta = get_object_or_404(Dieta, id=dietaID)
        
        alimento = get_object_or_404(Alimento, id=alimento)
        Pasto.objects.create(idDieta=dieta, idalimento=alimento, tipo=tipo, giorno=giorno_, qta=qta)
        
    return redirect('info_paziente', idPazienteSel=dieta.paziente.id)
    
def rimuovi_pasto(request,idPazienteSel, idPasto):
    print( idPasto, idPazienteSel)
    if request.method == 'POST':
        pasto=get_object_or_404(Pasto, id=idPasto)

        pasto.delete()
    return redirect('info_paziente', idPazienteSel)



def crea_appuntamento(request, idDottore):
    if request.method == 'POST':
        data_ora_date = request.POST.get('data_ora_date')
        data_ora_time = request.POST.get('data_ora_time')

        if data_ora_date and data_ora_time:
            try:
                data_ora_str = f"{data_ora_date} {data_ora_time}"
                data_ora = parse_datetime(data_ora_str)

                if not data_ora:
                    return JsonResponse({'success': False, 'error': 'Data e ora non valide.'})

                if timezone.is_naive(data_ora):
                    data_ora = timezone.make_aware(data_ora, timezone.get_current_timezone())

                if data_ora < timezone.now():
                    return JsonResponse({'success': False, 'error': 'Non puoi prenotare un appuntamento per una data passata.'})

                paziente = get_object_or_404(Utente, id=request.user.id)
                dottore = get_object_or_404(Utente, id=idDottore)

                if Appuntamento.objects.filter(Dottore=dottore, data_ora=data_ora).exists():
                    return JsonResponse({'success': False, 'error': 'Lo slot selezionato non è disponibile.'})

                Appuntamento.objects.create(
                    Dottore=dottore,
                    Paziente=paziente,
                    stato=0,
                    data_ora=data_ora
                )

                return JsonResponse({'success': True})

            except ValueError:
                return JsonResponse({'success': False, 'error': 'Data e ora non valide.'})

            except Exception as e:
                # Log dell'errore per il debugging
                print(f"Errore durante la creazione dell'appuntamento: {e}")
                return JsonResponse({'success': False, 'error': 'Si è verificato un errore durante la creazione dell\'appuntamento.'})

        else:
            return JsonResponse({'success': False, 'error': 'Data e ora mancanti.'})

    return JsonResponse({'success': False, 'error': 'Metodo non supportato.'})

@login_required(login_url='login')
def accettaAppuntamento(request, app_id):
    app = get_object_or_404(Appuntamento, id=app_id)
    
    if request.user.id != app.Dottore.id:
        return redirect('error_page') 
    
    app.stato = 1
    app.save()
    
    return redirect('home')  



@login_required(login_url='login')
def rifiutaAppuntamento(request, app_id):
    app = get_object_or_404(Appuntamento, id=app_id)
    
    if request.user.id != app.Dottore.id:
        return redirect('error_page')  
    app.stato = -1
    app.save()
    
    return redirect('home')  

@login_required(login_url='login')
def eliminaAppuntamento(request, app_id):
    app = get_object_or_404(Appuntamento, id=app_id)

    if request.user.tipo_utente:  
        app.stato = -1 
        app.save()  
    else:
        app.delete() 
    
    return redirect('home')

@require_POST
def modifica_appuntamento(request):
    if request.method == 'POST':
        appuntamento_id = request.POST.get('id')
        nuovo_orario = request.POST.get('time')

        if appuntamento_id and nuovo_orario:
            try:
                appuntamento = get_object_or_404(Appuntamento, id=appuntamento_id)

                # Aggiorna solo l'orario, mantenendo la data originale
                data_ora = appuntamento.data_ora
                ore, minuti = map(int, nuovo_orario.split(':'))
                nuovo_data_ora = data_ora.replace(hour=ore, minute=minuti)
                
                # Controlla se il nuovo orario è passato
                if nuovo_data_ora < timezone.now():
                    return JsonResponse({'success': False, 'error': 'Non puoi modificare l\'appuntamento a una data passata.'})

                # Controlla se lo slot è già occupato
                if Appuntamento.objects.filter(data_ora=nuovo_data_ora).exclude(id=appuntamento_id).exists():
                    return JsonResponse({'success': False, 'error': 'Lo slot selezionato non è disponibile.'})

                # Salva le modifiche
                appuntamento.data_ora = nuovo_data_ora
                appuntamento.stato= 0 # si passa in elaborazione
                appuntamento.save()

                return JsonResponse({'success': True})

            except ValueError:
                return JsonResponse({'success': False, 'error': 'Orario non valido.'})

            except Exception as e:
                return JsonResponse({'success': False, 'error': 'Si è verificato un errore durante la modifica dell\'orario.'})

        return JsonResponse({'success': False, 'error': 'Orario o ID mancanti.'})

    return JsonResponse({'success': False, 'error': 'Metodo non supportato.'})
    



@login_required(login_url='login')
def calendario(request):

    month_offset = int(request.GET.get('month', 0))


    today = datetime.date.today()
    first_day_of_month = (today.replace(day=1) + timedelta(days=month_offset * 30)).replace(day=1)
    last_day_of_month = first_day_of_month.replace(day=monthrange(first_day_of_month.year, first_day_of_month.month)[1])

    if request.user.tipo_utente is False:
        appuntamenti = Appuntamento.objects.filter(
            Paziente_id=request.user,
            data_ora__range=[first_day_of_month, last_day_of_month]
        ).order_by('data_ora')
    else:
         appuntamenti = Appuntamento.objects.filter(
            Dottore_id=request.user,
            data_ora__range=[first_day_of_month, last_day_of_month]
        ).order_by('data_ora')


    days_range = [first_day_of_month + timedelta(days=i) for i in range(last_day_of_month.day)]

    context = {
        'appuntamenti': appuntamenti,
        'days_range': days_range,
        'month_offset': month_offset,
        'first_day_of_month': first_day_of_month,
    }
    
    return context

@login_required
def edit_studio(request):
    try:
        
        studio = Studio.objects.get(medico=request.user)
    except Studio.DoesNotExist:
      
        studio = None

    if request.method == 'POST':
        form = StudioForm(request.POST, instance=studio)
        if form.is_valid():
            studio_instance = form.save(commit=False)
            studio_instance.medico = request.user
            studio_instance.save()
            return redirect('home')
    else:
        form = StudioForm()

    return redirect('home')

from django.http import JsonResponse

@login_required
def chats(request, receiver=None):
    if request.user.is_authenticated:
        if request.user.tipo_utente:  
            user_chats = Chat.objects.filter(participants=request.user).distinct()
            medici = []
        else:  
            cure = Cura.objects.filter(idPaziente=request.user, statoRichiesta=1)  # statoRichiesta=1 indica che la richiesta è accettata
            medici = [cura.idDottore for cura in cure]
            
            if receiver:
                medico = get_object_or_404(Utente, id=receiver, tipo_utente=True)
                chat = Chat.objects.filter(participants__in=[request.user, medico]).distinct().first()
                
                if not chat:
                    chat = Chat.objects.create()
                    chat.participants.add(request.user, medico)
                    chat.save()
                
                return JsonResponse({'chat_id': chat.id})

            user_chats = Chat.objects.filter(participants=request.user).filter(participants__in=medici).distinct()
    
    else:
        user_chats = []
        medici = []

    return render(request, 'chat.html', {
        'chats': user_chats,
        'medici': medici,
    })

@login_required
def chat_details(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    messages = chat.messages.order_by('timestamp')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        messages_data = [message.serialize() for message in messages]
        return JsonResponse({'messages': messages_data})

    return render(request, 'chat_details.html', {
        'chat': chat,
        'messages': messages,
    })

@csrf_exempt
def add_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        chat_id = data['chat_id']
        content = data['messageText']

        chat = Chat.objects.get(id=chat_id)
        message = Message.objects.create(
            chat=chat,
            sender=request.user,
            content=content
        )

        response_data = {
            'sender': {
                'username': request.user.username
            },
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

        return JsonResponse(response_data)