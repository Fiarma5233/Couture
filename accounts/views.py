from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.db import IntegrityError  # Pour la gestion des erreurs liees a l'integrite des donnees

from .models import Couturier, Client, Commande, Facture
from django.contrib.auth.models import User  # Pour la creation d'utilisateurs
from django.contrib.auth import authenticate, login, logout # Pour conexion, deconnexion et authentification
from Couture import settings  # Pour avoir acces elements pour l'envoi du mail se trouvant dans settings
from django.core.mail import send_mail, EmailMessage  # Pour l'envoi du mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
# instaler six : pip install six
from django.contrib.sites.shortcuts import get_current_site
from .token import generatorToken # importation de l'instance de classe TokenGenerator depuis le fichier token.py
from django.contrib import messages # Pour generer les messages d'erreur ou de succes
from datetime import datetime, timedelta # Sera utiliser pour l'historique
from django.core.paginator import Paginator  #  Pour la pagination
from django.utils import timezone  # Pour l'historique
#from decimal import Decimal
#from django.http import FileResponse  # Pour telecharger la facture

#  Pour conversion de html en pdf
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.



def home(request):
    if request.method == 'GET':
        dir = {
           "greeting": "Vous etes la bienvenue"
        }
        return render(request, "accounts/Home.html")
#    return render(request, "accounts/Home.html", dir)

'''
    Lastname = request.POST.get('Lastname')
    Firstname = request.POST.get('Firstname')
    Company = request.POST.get("Company")
    Email = request.POST.get("Email")
    Password = request.POST.get("Password")
    PasswordConfirm = request.POST.get(" PasswordConfirm")
    couturier = Couturier.objects.create(Lastname=Lastname ,  Firstname=Firstname, Company=Company, Email=Email, Password=Password, PasswordConfirm=PasswordConfirm )                   # Appel de notre model
    couturier.save() # Enregistrement de nos donnees dans la db

    '''
    

'''def inscription(request):
    if request.method =="GET":

        contexte = {
            "titre1": "Inscription",
            "message" : "Bonsoir",
            }
        return render (request, "accounts/Inscription.html")
    
    
    if request.method == 'POST':
    # Recuperation des donnees entrees par l'utilisateur
        Lastname = request.POST.get('Lastname')
       
        Firstname = request.POST.get('Firstname')
        Company = request.POST.get("Company")
        Email = request.POST.get("Email")
        Password = request.POST.get("Password")
        PasswordConfirm = request.POST.get(" PasswordConfirm")
        couturier = Couturier.objects.create(Lastname=Lastname ,  Firstname=Firstname, Company=Company, Email=Email, Password=Password, PasswordConfirm=PasswordConfirm )                   # Appel de notre model
        couturier.save() # Enregistrement de nos donnees dans la db
        messages.success(request, 'Votre compte a ete creee avec succes')
        return redirect('accounts:connexion')

                             
    return render(request, "accounts/Inscription.html", contexte)'''


'''msg = {
    "salut" :"Vous etes connectes"
}'''

'''if request.method == "POST":
    Company = request.POST.get("Company")
    Password = request.POST.get("Password")
    # verification avec la methode 
    user = authenticate(Company=Company, Password=Password)

    # Verifions si l'utilisateur existe 
    if user is not None:
        login(request, user)
        firstname = Couturier.Firstname
        return render( request, "accounts/Home.html", {"firstname" : firstname})
    else:
        messages.error(request, "Mauvaise authentification")
        return redirect('accounts:connexion')'''
    

'''def connexion(request):
    if request.method == "GET":
        couturier = Couturier.objects.all()
        return render (request, "accounts/Connexion.html", {"couturier" : couturier})
    
    if request.method == 'POST':
        Company = request.POST["Company"]
        Password = request.POST["Password"]
        # verification avec la methode 
        user = authenticate(Company=Company, Password=Password)

        # Verifions si l'utilisateur existe 
        if user is not None:
            login(request, user)
            firstname = user.Firstname
            return  render(request, "accounts/ListeCommande.html", {"firstname" : firstname}) #render(request, "accounts/Home.html", {"firstname" : firstname})
        else:
            messages.error(request, "Mauvaise authentification")
            return redirect('accounts:connexion')
    return render(request, 'accounts/Connexion.html')'''


def inscription(request):
    if request.method =="GET":

        contexte = {
            "titre1": "Inscription",
            "message" : "Bonsoir",
            }
        return render (request, "accounts/Inscription.html")
    
    
    if request.method == 'POST':
    # Recuperation des donnees entrees par l'utilisateur
        lastname = request.POST.get('lastname')
       
        firstname = request.POST.get('firstname')
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")

        if User.username == "":
            messages.error(request, "Veuillez remplir ce champ")
            return redirect("accounts:inscription")

        if User.objects.filter(username=username):
            messages.error(request, "Ce nom existe deja")
            return redirect("inscription")
        
        if User.objects.filter(email=email):
            messages.error(request, "Cet email a deja un compte")
            return redirect("inscription")
        
        if password != password1 :
            messages.error(request, "Les deux mots de passe doivent etre les memes")
            return redirect("accounts:inscription")
        #couturier = Couturier.objects.create(Lastname=Lastname ,  Firstname=Firstname, Company=Company, Email=Email, Password=Password, PasswordConfirm=PasswordConfirm )                   # Appel de notre model
        couturier = User.objects.create_user( username, email, password )                   # Appel de notre model
        couturier.first_name = firstname
        couturier.last_name = lastname
        #couturier.password= Password

        couturier.is_active = False # Utilisateur non active
        couturier.save() # Enregistrement de nos donnees dans la db
        messages.success(request, 'Votre compte a ete creee avec succes')

        #   Email de Bienvenue
        subject = "Soyez la bienvenue a l'entreprise "  + username + '!!!'     # Sujet de notre mail
        message = "Bienvenu " + couturier.first_name + " " + couturier.last_name + "\n\n\n Fiarma SOME"  #Message a envoyer
        form_email = settings.EMAIL_HOST_USER  # Adrresse mail qui va envoyer le mail
        to_list = [couturier.email]  # Destinataire du mail
        send_mail(subject, message, form_email, to_list, fail_silently=False) # Envoi du mail

        # Email de confirmation
        current_site = get_current_site(request)  # Pour avoir le lien du site
        email_subject = "Confirmation de l'addresse email sur " + username  # Sujet du mail
        messageConfirm = render_to_string("emailConfirm.html", {
            "name" : couturier.first_name,  # Prenom de l'utilisateur
            "domain": current_site.domain,  # Nom du domaine (site)
            "uid" :urlsafe_base64_encode(force_bytes(couturier.pk)), # Donner un id chaque lien endode sur64 bits
            "token": generatorToken.make_token(couturier)
        }) # Confirmation du message dans un fichier

        # Pour envoi
        email = EmailMessage(
            email_subject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [couturier.email]
        )

        email.fail_silently = False  #  Ceci permet d'indiquer les eventuelles erreurs liees a l'envoi du mail
        email.send() # Envoi




        return redirect('connexion')

                             
    return render(request, "accounts/Inscription.html", contexte)

def activate(request, uidb64, token): # cette fonction genere le lien de confimation unique a chaque utilisateur
    try:
        # Verifions si le lien correspond a l'utilisateur en question
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True  # C'est lorsqu'on clique sur le lien de confirmation que l'utilisateur est actif
        user.save() # On l'enrregistre
        messages.success(request, "Congratulations !!! Votre compte a ete activated")
        return redirect("connexion")
    
    else:
        messages.error(request, "Echec d'activation de votre compte. Reessayer plutard !!!")
        return redirect("accounts:home")


def connexion(request):
    '''if request.method == "GET":
        couturier = Couturier.objects.all()
        return render (request, "accounts/Connexion.html", {"couturier" : couturier})'''
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST["password"]
        # verification avec la methode 
        user = authenticate(username=username, password=password)
        try:
            my_user = User.objects.get(username=username)

        except User.DoesNotExist:
            messages.error(request, "Ce compte n'existe pas")
            return redirect("connexion")

        # Verifions si l'utilisateur existe 
        if user is not None:
            login(request, user)
            firstname = user.first_name
            return  render(request, "accounts/ListeCommande.html", {"firstname" : firstname}) #render(request, "accounts/Home.html", {"firstname" : firstname})
        
        #elif my_user.username.DoesNotExist:
            
        
        elif my_user.is_active == False:  # Si l'utilisateur tente de se connecter sans avoir confirmer  son addresse
            messages.error(request, "Vous n'avez pas encore confirme votre addresse email. Faites-le avant de vous connecter !!!")
        else:
            messages.error(request, "Mauvaise authentification")
            return redirect('connexion')
        
       

    return render(request, 'accounts/Connexion.html')



def deconnexion(request):
    logout(request)
    messages.success(request, "Vous avez ete deconnecte")
    return redirect("home")


# Pour confirmer le mot de passe renitialise

def confirmer(request, *args, **kwargs):
    #.objects.get(email=email)

    if request.method == "GET":
        return render(request, 'accounts/password-reset-confirm.html')
    
    if request.method == "POST":
        password = request.POST.get("password")
        password1 = request.POST.get("password1")

        couturiers = User.objects.all()

        #couturier = couturiers.objects.get(email=email)
        if password != password1 :
            messages.error(request, "Les deux mots de passe doivent etre les memes")
            return redirect("confirmer")
        User.password=password
        User.save()
        messages.success(request, "Vous venez de modifier votre mot de passe")
    return render(request, 'accounts/connexion')

# Recuperation des donnees du Client
def client(request):
    if request.method =="GET":
        '''if request.method == "GET":
            return render(request, "accounts/Client.html") 
        
        if request.method == "POST":
            Nom = request.POST.get("Nom")
            #Prenom = request.POST.get("Prenom")
            Telephone = request.POST.get("Telephone")
            client = Client.objects.create(Nom=Nom,  Telephone=Telephone)
            client.save()
            msg = messages.success(request, "Inscription reussie")
            return redirect('accounts:commande')'''
        clients =  Client.objects.all()


        #commandes = Commande.objects.all().order_by("-Date_Depot_Model")   # Recuperation des commandes selon la date de prise de commande
        pagination = Paginator(clients, 5)  # Affichage de  5 commandes par pages
        page = request.GET.get('page') # obtention de la page
        clients_page = pagination.get_page(page)
        customer ={"clients_page" : clients_page}

        return render(request, 'accounts/Client.html', customer)




# Recuperation des donnees de la  commande (  CE QUI FONCTIONNE )
'''def commande(request):
    if request.method == "GET":
        client = Client.objects.all()
        contest = { ' clients ' : client}
        return render(request, "accounts/Commande.html", contest)
    
    if request.method == "POST":
        
        Nom = request.POST.get("Nom")
        Telephone = request.POST.get("Telephone")
        #Client = request.POST.get("Client")
        Modele_Couture = request.POST.get("Modele_Couture")
        Nombre_Pagnes = request.POST.get("Nombre_Pagnes")
        Dos = request.POST.get("Dos")
        Epaule = request.POST.get("Epaule")
        Poitrine = request.POST.get("Poitrine")
        Longueur_Manche = request.POST.get("Longueur_Manche")
        Tour_Manche = request.POST.get("Tour_Manche")
        Longueur_Taille = request.POST.get("Longueur_Taille")
        Tour_Taille = request.POST.get("Tour_Taille")
        Pince_longueur_seins = request.POST.get("Pince_longueur_seins")
        Longueur_Camisole = request.POST.get("Longueur_Camisole")
        Longueur_Robe = request.POST.get("Longueur_Robe")
        Longueur_Chemise = request.POST.get("Longueur_Chemise")
        Messure_Bassin = request.POST.get("Messure_Bassin")
        Mesure_Ceinture = request.POST.get("Mesure_Ceinture")
        Mesure_Cuisse = request.POST.get("Mesure_Cuisse")
        Mesure_Genoux = request.POST.get("Mesure_Genoux")
        Longeur_Jupe = request.POST.get("Longeur_Jupe")
        Longueur_Bras = request.POST.get("Longueur_Bras")
        Longueur_Poignet = request.POST.get("Longueur_Poignet")
        Prix_Couture = request.POST.get("Prix_Couture")
        Avance = request.POST.get("Avance")
        Date_Depot_Model = request.POST.get("Date_Depot_Model")
        Date_Retrait_Model = request.POST.get("Date_Retrait_Model")


        # verifions si le client existe
        try:
            
            client = Client.objects.get(Telephone=Telephone)
            #client.Interventions += 1
            Client.Nom=Nom
            client.save()
        
        except Client.DoesNotExist:
            try:
                client = Client.objects.create(Nom=Nom, Telephone=Telephone, Interventions=0)
                client.save()

            except IntegrityError:
                client=  Client.objects.get(Telephone=Telephone)
        
        commande = Commande.objects.create(client=client, Nom=Nom, Telephone=Telephone, Modele_Couture=Modele_Couture, Nombre_Pagnes=Nombre_Pagnes, Dos=Dos, Epaule=Epaule, Poitrine=Poitrine, Longueur_Manche=Longueur_Manche, Tour_Manche=Tour_Manche , Longueur_Taille=Longueur_Taille, Tour_Taille=Tour_Taille, Pince_longueur_seins=Pince_longueur_seins, Longueur_Camisole=Longueur_Camisole, Longueur_Robe=Longueur_Robe, Longueur_Chemise=Longueur_Chemise, Messure_Bassin=Messure_Bassin, Mesure_Ceinture=Mesure_Ceinture, Mesure_Cuisse=Mesure_Cuisse, Mesure_Genoux=Mesure_Genoux, Longeur_Jupe=Longeur_Jupe, Longueur_Bras=Longueur_Bras, Longueur_Poignet=Longueur_Poignet, Prix_Couture=Prix_Couture, Avance=Avance, Date_Depot_Model=Date_Depot_Model, Date_Retrait_Model=Date_Retrait_Model)
        
        commande.save()

       
        
        
# Creation d'une facture
        Prix_Couture=float(request.POST.get('Prix_Couture'))  # Pour convertir les valeur qui sont de type string en float afin d'effecturerles operations(calcul du solde)
        Avance=float(request.POST.get('Avance'))
        Solde=Prix_Couture - Avance
        

        
       
        facture = Facture.objects.create(
            command=commande,
            Nom=Nom,
            Telephone=Telephone,
            Modele_couture=Modele_Couture,
            Prix_Couture=Prix_Couture,
            Avance=Avance,
            Solde=Solde

        )
        facture.save()
        #commande.save()
        client.Interventions += 1
        client.save()


        messages.success(request, "Commande ajoutee avec succes")
        return redirect('accounts:liste_commande')
   

    return render(request, "accounts/Commande.html") '''






def commande(request):

    nomError = None
    telError = None
    modele = None
    pagne = None
    dos = None
    epaule = None
    poitrine = None
    lgm = None
    trm = None
    lgt = None
    col = None
    trt = None
    pls = None
    lgc = None
    lgr = None
    frappe = None
    lgch = None
    mb = None
    mc = None
    mcu = None
    mg = None
    lgj = None
    lgpo = None
    lgpa =None
    bas = None
    pc = None
    avance = None


    dateError = None

    if request.method == "GET":
        client = Client.objects.all()
        contest = { ' clients ' : client}
        return render(request, "accounts/Commande.html", contest)
    
    #nomError = None
    #telError = None
    #pagneError = None

    if request.method == "POST":
    
        

        Nom = request.POST.get("Nom")
        Telephone = request.POST.get("Telephone")
        #Client = request.POST.get("Client")
        Modele_Couture = request.POST.get("Modele_Couture")
        Nombre_Pagnes = request.POST.get("Nombre_Pagnes")
        Dos = request.POST.get("Dos")

        
        Epaule = request.POST.get("Epaule")
        Poitrine = request.POST.get("Poitrine")
        Longueur_Manche = request.POST.get("Longueur_Manche")
        Tour_Manche = request.POST.get("Tour_Manche")
        Longueur_Taille = request.POST.get("Longueur_Taille")
        Col = request.POST.get("Col") 


        Tour_Taille = request.POST.get("Tour_Taille")
        Pince_longueur_seins = request.POST.get("Pince_longueur_seins")
        Longueur_Camisole = request.POST.get("Longueur_Camisole")
        Longueur_Robe = request.POST.get("Longueur_Robe")
        Frappe = request.POST.get("Frappe")
        Longueur_Chemise = request.POST.get("Longueur_Chemise")

        Messure_Bassin = request.POST.get("Messure_Bassin")
        Mesure_Ceinture = request.POST.get("Mesure_Ceinture")
        Mesure_Cuisse = request.POST.get("Mesure_Cuisse")
        Mesure_Genoux = request.POST.get("Mesure_Genoux")
        Longeur_Jupe = request.POST.get("Longeur_Jupe")
        Longueur_Poignet = request.POST.get("Longueur_Poignet")

        Longueur_Pantalon = request.POST.get("Longueur_Pantalon")
        Bas =  request.POST.get("Bas")

        Prix_Couture = request.POST.get("Prix_Couture")
        Avance = request.POST.get("Avance")
        Date_Depot_Model = request.POST.get("Date_Depot_Model")
        Date_Retrait_Model = request.POST.get("Date_Retrait_Model")


        # Controle de donnees

        if Nom == '':
            nomError = 'Ce champ ne doit pas etre vide'
            return render(request, "accounts/Commande.html", {"nomError": nomError})

        if Telephone == '' or int(Telephone) < 0 or len(Telephone) < 8 or len(Telephone) >= 10:
            #or Telephone < 0  or Telephone.length < 8 
            telError = 'Votre numero doit avoir 8 chiffres'
            return render(request, "accounts/Commande.html", {"telError": telError})
        
        if Modele_Couture == '':
            modele = 'Ce champ ne doit pas etre vide'
            return render(request, "accounts/Commande.html", {"modele": modele})

        if  not Nombre_Pagnes.isnumeric() or Nombre_Pagnes == '' or  int(Nombre_Pagnes) <= 0 :
            pagne = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"pagne": pagne})

        if  not Dos.isnumeric() or Dos == '' or  int(Dos) <= 0 :
            dos = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"dos": dos})
        
        if  not Epaule.isnumeric() or epaule == '' or  int(Epaule) <= 0 :
            epaule = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"epaule": epaule})




        '''if  not Epaule.isnumeric() or Epaule == '' or  int(Epaule) <= 0 :
            pagneError = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"pagneError": pagneError})'''

        if  not Poitrine.isnumeric() or Poitrine == '' or  int(Poitrine) <= 0 :
            poitrine = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"poitrine": poitrine})


        if  not Longueur_Manche.isnumeric() or Longueur_Manche == '' or  int(Longueur_Manche) <= 0 :
            lgm = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"lgm": lgm})


        if  not Tour_Manche.isnumeric() or Tour_Manche == '' or  int(Tour_Manche) <= 0 :
            trm = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"trm": trm})


        if  not Longueur_Taille.isnumeric() or Longueur_Taille == '' or  int(Longueur_Taille) <= 0 :
            lgt = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"lgt": lgt})


        if  not Col.isnumeric() or Col == '' or  int(Col) <= 0 :
                col = 'Donnez un nombre qui depasse 0'
                return render(request, "accounts/Commande.html", {"col": col})


        if  not Tour_Taille.isnumeric() or Tour_Taille == '' or  int(Tour_Taille) <= 0 :
                trt = 'Donnez un nombre qui depasse 0'
                return render(request, "accounts/Commande.html", {"trt": trt})


        if  not Pince_longueur_seins.isnumeric() or Pince_longueur_seins == '' or  int(Pince_longueur_seins) <= 0 :
                pls = 'Donnez un nombre qui depasse 0'
                return render(request, "accounts/Commande.html", {"pls": pls})


        if  not Longueur_Camisole.isnumeric() or Longueur_Camisole == '' or  int(Longueur_Camisole) <= 0 :
                lgc = 'Donnez un nombre qui depasse 0'
                return render(request, "accounts/Commande.html", {"lgc": lgc})


        if  not Longueur_Robe.isnumeric() or Longueur_Robe == '' or  int(Longueur_Robe) <= 0 :
                lgr = 'Donnez un nombre qui depasse 0'
                return render(request, "accounts/Commande.html", {"lgr": lgr})


        if  not Frappe.isnumeric() or Frappe == '' or  int(Frappe) <= 0 :
                frappe = 'Donnez un nombre qui depasse 0'
                return render(request, "accounts/Commande.html", {"frappe": frappe})


        if  not Longueur_Chemise.isnumeric() or Longueur_Chemise == '' or  int(Longueur_Chemise) <= 0 :
                lgch = 'Donnez un nombre qui depasse 0'
                return render(request, "accounts/Commande.html", {"lgch": lgch})


        if  not Messure_Bassin.isnumeric() or Messure_Bassin == '' or  int(Messure_Bassin) <= 0 :
            mb = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"mb": mb})


        if  not Mesure_Ceinture.isnumeric() or Mesure_Ceinture == '' or  int(Mesure_Ceinture) <= 0 :
            mc = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"mc": mc})


        if  not Mesure_Cuisse.isnumeric() or Mesure_Cuisse == '' or  int(Mesure_Cuisse) <= 0 :
            mcu = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"mcu": mcu})


        if  not Mesure_Genoux.isnumeric() or Mesure_Genoux == '' or  int(Mesure_Genoux) <= 0 :
            mg = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"mg": mg})


        if  not Longeur_Jupe.isnumeric() or Longeur_Jupe == '' or  int(Longeur_Jupe) <= 0 :
            lgj = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"lgj": lgj})



        if  not Longueur_Poignet.isnumeric() or Longueur_Poignet == '' or  int(Longueur_Poignet) <= 0 :
            lgpo = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"lgpo": lgpo})


        if  not Longueur_Pantalon.isnumeric() or Longueur_Pantalon == '' or  int(Longueur_Pantalon) <= 0 :
            lgpa = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"lgpa": lgpa})



        if  not Bas.isnumeric() or Bas == '' or  int(Bas) <= 0 :
            bas = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"bas": bas})



        if  not Prix_Couture.isnumeric() or Prix_Couture == '' or  int(Prix_Couture) <= 0 :
            pc = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"pc": pc})


        if  not Avance.isnumeric() or Avance == '' or  int(Avance) <= 0 :
            avance = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"avance": avance})


            
        if Date_Retrait_Model == '':
            dateError = "Entrez une date valide.Exemple : \t 2025-12-25"
            return render(request, "accounts/Commande.html", {"dateError": dateError})
            
        # Fin

        
        # verifions si le client existe
        try:
            
            client = Client.objects.get(Telephone=Telephone)
            #client.Interventions += 1
            Client.Nom=Nom
            client.save()
        
        except Client.DoesNotExist:
            try:
                client = Client.objects.create(Nom=Nom, Telephone=Telephone, Interventions=0)
                client.save()

            except IntegrityError:
                client=  Client.objects.get(Telephone=Telephone)
        
        commande = Commande.objects.create(
            client=client,

            Nom=Nom, 
            Telephone=Telephone, 
            Modele_Couture=Modele_Couture, 
            Nombre_Pagnes=Nombre_Pagnes, 
            Dos=Dos, 
            Epaule=Epaule,
            Poitrine=Poitrine, 

            Longueur_Manche=Longueur_Manche,
            Tour_Manche=Tour_Manche , 
            Longueur_Taille=Longueur_Taille, 
            Col=Col,  #
            Tour_Taille=Tour_Taille, 
            Pince_longueur_seins=Pince_longueur_seins, 
            Longueur_Camisole=Longueur_Camisole, 

            Longueur_Robe=Longueur_Robe, 
            Frappe=Frappe,
            Longueur_Chemise=Longueur_Chemise, 
            Messure_Bassin=Messure_Bassin, 
            Mesure_Ceinture=Mesure_Ceinture, 
            Mesure_Cuisse=Mesure_Cuisse, 
            Mesure_Genoux=Mesure_Genoux, 
            
            Longeur_Jupe=Longeur_Jupe, 
            Longueur_Poignet=Longueur_Poignet, 
            Longueur_Pantalon=Longueur_Pantalon, 
            Bas=Bas,
            Prix_Couture=Prix_Couture, 
            Avance=Avance,
            Date_Depot_Model=Date_Depot_Model, 
            Date_Retrait_Model=Date_Retrait_Model)
        
        commande.save()
        
    # Creation d'une facture
        Prix_Couture=float(request.POST.get('Prix_Couture'))  # Pour convertir les valeur qui sont de type string en float afin d'effecturerles operations(calcul du solde)
        Avance=float(request.POST.get('Avance'))
        Solde=Prix_Couture - Avance
        facture = Facture.objects.create(
            command=commande,
            Nom=Nom,
            Telephone=Telephone,
            Modele_couture=Modele_Couture,
            Prix_Couture=Prix_Couture,
            Avance=Avance,
            Solde=Solde

        )
        facture.save()
        #commande.save()
        client.Interventions += 1
        client.save()


        messages.success(request, "Commande ajoutee avec succes")
        return redirect('liste_commande')



    return render(request, "accounts/Commande.html") 


  
# Liste des commandes
def liste_commande(request):

    commandes = Commande.objects.all().order_by("-Date_Depot_Model")   # Recuperation des commandes selon la date de prise de commande
    pagination = Paginator(commandes, 5)  # Affichage de  5 commandes par pages
    page = request.GET.get('page') # obtention de la page
    commandes_page = pagination.get_page(page)
    cmd ={"commandes_page" : commandes_page}



    return render(request, 'accounts/ListeCommande.html', cmd)



# Modification d'une commande
def modifier_commande(request, commande_id):


    nomError = None
    telError = None
    modele = None
    pagne = None
    dos = None
    epaule = None
    poitrine = None
    lgm = None
    trm = None
    lgt = None
    col = None
    trt = None
    pls = None
    lgc = None
    lgr = None
    frappe = None
    lgch = None
    mb = None
    mc = None
    mcu = None
    mg = None
    lgj = None
    lgpo = None
    lgpa =None
    bas = None
    pc = None
    avance = None


    dateError = None


    if request.method == "GET":
        commande = get_object_or_404(Commande, id=commande_id)
        #commande = Commande.objects.filter(id=commande_id)
        contex = {'commande' : commande}
       
        return render(request, 'accounts/ModifierCommande.html', contex )
    
    commande = get_object_or_404(Commande, id=commande_id) # Pour recuperer la commande en question
    facture = Facture.objects.get(command = commande_id)  # Pour recurer la facture liee a la commande
    #client = Client.objects.get(Telephone=commande.Telephone)
    client = Client.objects.get(Telephone=commande.Telephone)

    # partie  pour modifier

    if request.method == "POST":
        #Commande.commande_id=client ,
        Nom = request.POST.get("Nom")
        Telephone = request.POST.get("Telephone")
        #Client = request.POST.get("Client")
        Modele_Couture = request.POST.get("Modele_Couture")
        Nombre_Pagnes = request.POST.get("Nombre_Pagnes")
        Dos = request.POST.get("Dos")
        Epaule = request.POST.get("Epaule")
        Poitrine = request.POST.get("Poitrine")
        Longueur_Manche = request.POST.get("Longueur_Manche")
        Tour_Manche = request.POST.get("Tour_Manche")
        Longueur_Taille = request.POST.get("Longueur_Taille")
        Col = request.POST.get("Col") 

        Tour_Taille = request.POST.get("Tour_Taille")
        Pince_longueur_seins = request.POST.get("Pince_longueur_seins")
        Longueur_Camisole = request.POST.get("Longueur_Camisole")
        Longueur_Robe = request.POST.get("Longueur_Robe")
        Frappe = request.POST.get("Frappe")

        Longueur_Chemise = request.POST.get("Longueur_Chemise")
        Messure_Bassin = request.POST.get("Messure_Bassin")
        Mesure_Ceinture = request.POST.get("Mesure_Ceinture")
        Mesure_Cuisse = request.POST.get("Mesure_Cuisse")
        Mesure_Genoux = request.POST.get("Mesure_Genoux")
        Longeur_Jupe = request.POST.get("Longeur_Jupe")
        #Longueur_Bras = request.POST.get("Longueur_Bras")
        Longueur_Poignet = request.POST.get("Longueur_Poignet")
        Longueur_Pantalon = request.POST.get("Longueur_Pantalon")
        Bas =  request.POST.get("Bas")

        Prix_Couture = request.POST.get("Prix_Couture")
        Avance = request.POST.get("Avance")
        Date_Retrait_Model = request.POST.get("Date_Retrait_Model")
        #solde = Decimal(Prix_Couture) - Decimal(Avance)
        #  = 



# Controle de donnees

        if Nom == '':
            nomError = 'Ce champ ne doit pas etre vide'
            return render(request, "accounts/ModifierCommande.html", {"nomError": nomError})

        if Telephone == '' or int(Telephone) < 0 or len(Telephone) < 8 or len(Telephone) >= 10:
            #or Telephone < 0  or Telephone.length < 8 
            telError = 'Votre numero doit avoir 8 chiffres'
            return render(request, "accounts/ModifierCommande.html", {"telError": telError})
        
        if Modele_Couture == '':
            modele = 'Ce champ ne doit pas etre vide'
            return render(request, "accounts/ModifierCommande.html", {"modele": modele})

        if  not Nombre_Pagnes.isnumeric() or Nombre_Pagnes == '' or  int(Nombre_Pagnes) <= 0 :
            pagne = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"pagne": pagne})

        if  not Dos.isnumeric() or Dos == '' or  int(Dos) <= 0 :
            dos = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"dos": dos})
        
        if  not Epaule.isnumeric() or epaule == '' or  int(Epaule) <= 0 :
            epaule = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"epaule": epaule})




        '''if  not Epaule.isnumeric() or Epaule == '' or  int(Epaule) <= 0 :
            pagneError = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/Commande.html", {"pagneError": pagneError})'''

        if  not Poitrine.isnumeric() or Poitrine == '' or  int(Poitrine) <= 0 :
            poitrine = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"poitrine": poitrine})


        if  not Longueur_Manche.isnumeric() or Longueur_Manche == '' or  int(Longueur_Manche) <= 0 :
            lgm = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"lgm": lgm})


        if  not Tour_Manche.isnumeric() or Tour_Manche == '' or  int(Tour_Manche) <= 0 :
            trm = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"trm": trm})


        if  not Longueur_Taille.isnumeric() or Longueur_Taille == '' or  int(Longueur_Taille) <= 0 :
            lgt = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"lgt": lgt})


        if  not Col.isnumeric() or Col == '' or  int(Col) <= 0 :
                col = 'Donnez un nombre qui depasse 0'
                return render(request, "accounts/ModifierCommande.html", {"col": col})


        if  not Tour_Taille.isnumeric() or Tour_Taille == '' or  int(Tour_Taille) <= 0 :
                trt = 'Donnez un nombre qui depasse 0'
                return render(request, "accounts/ModifierCommande.html", {"trt": trt})


        if  not Pince_longueur_seins.isnumeric() or Pince_longueur_seins == '' or  int(Pince_longueur_seins) <= 0 :
                pls = 'Donnez un nombre qui depasse 0'
                return render(request, "accounts/ModifierCommande.html", {"pls": pls})


        if  not Longueur_Camisole.isnumeric() or Longueur_Camisole == '' or  int(Longueur_Camisole) <= 0 :
                lgc = 'Donnez un nombre qui depasse 0'
                return render(request, "accounts/ModifierCommande.html", {"lgc": lgc})


        if  not Longueur_Robe.isnumeric() or Longueur_Robe == '' or  int(Longueur_Robe) <= 0 :
                lgr = 'Donnez un nombre qui depasse 0'
                return render(request, "accounts/ModifierCommande.html", {"lgr": lgr})


        if  not Frappe.isnumeric() or Frappe == '' or  int(Frappe) <= 0 :
                frappe = 'Donnez un nombre qui depasse 0'
                return render(request, "accounts/ModifierCommande.html", {"frappe": frappe})


        if  not Longueur_Chemise.isnumeric() or Longueur_Chemise == '' or  int(Longueur_Chemise) <= 0 :
                lgch = 'Donnez un nombre qui depasse 0'
                return render(request, "accounts/ModifierCommande.html", {"lgch": lgch})


        if  not Messure_Bassin.isnumeric() or Messure_Bassin == '' or  int(Messure_Bassin) <= 0 :
            mb = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"mb": mb})


        if  not Mesure_Ceinture.isnumeric() or Mesure_Ceinture == '' or  int(Mesure_Ceinture) <= 0 :
            mc = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"mc": mc})


        if  not Mesure_Cuisse.isnumeric() or Mesure_Cuisse == '' or  int(Mesure_Cuisse) <= 0 :
            mcu = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"mcu": mcu})


        if  not Mesure_Genoux.isnumeric() or Mesure_Genoux == '' or  int(Mesure_Genoux) <= 0 :
            mg = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"mg": mg})


        if  not Longeur_Jupe.isnumeric() or Longeur_Jupe == '' or  int(Longeur_Jupe) <= 0 :
            lgj = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"lgj": lgj})



        if  not Longueur_Poignet.isnumeric() or Longueur_Poignet == '' or  int(Longueur_Poignet) <= 0 :
            lgpo = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"lgpo": lgpo})


        if  not Longueur_Pantalon.isnumeric() or Longueur_Pantalon == '' or  int(Longueur_Pantalon) <= 0 :
            lgpa = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"lgpa": lgpa})



        if  not Bas.isnumeric() or Bas == '' or  int(Bas) <= 0 :
            bas = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"bas": bas})



        if  not Prix_Couture.isnumeric() or Prix_Couture == '' or  int(Prix_Couture) <= 0 :
            pc = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"pc": pc})


        if  not Avance.isnumeric() or Avance == '' or  int(Avance) <= 0 :
            avance = 'Donnez un nombre qui depasse 0'
            return render(request, "accounts/ModifierCommande.html", {"avance": avance})


            
        if Date_Retrait_Model == '':
            dateError = "Entrez une date valide.Exemple : \t 2025-12-25"
            return render(request, "accounts/ModifierCommande.html", {"dateError": dateError})
            
        # Fin



        commande.Nom = Nom
        commande.Telephone = Telephone
        #Client = request.POST.get("Client")
        commande.Modele_Couture = Modele_Couture
        commande.Nombre_Pagnes = Nombre_Pagnes
        commande.Dos = Dos
        commande.Epaule = Epaule
        commande.Poitrine = Poitrine
        commande.Longueur_Manche = Longueur_Manche
        commande.Tour_Manche = Tour_Manche
        commande.Longueur_Taille = Longueur_Taille
        commande.Col = Col

        commande.Tour_Taille = Tour_Taille
        commande.Pince_longueur_seins = Pince_longueur_seins
        commande.Longueur_Camisole = Longueur_Camisole
        commande.Longueur_Robe = Longueur_Robe
        commande.Frappe = Frappe

        commande.Longueur_Chemise = Longueur_Chemise
        commande.Messure_Bassin = Messure_Bassin
        commande.Mesure_Ceinture = Mesure_Ceinture
        commande.Mesure_Cuisse = Mesure_Cuisse
        commande.Mesure_Genoux = Mesure_Genoux
        commande.Longeur_Jupe = Longeur_Jupe
       # commande.Longueur_Bras = Longueur_Bras
        commande.Longueur_Poignet = Longueur_Poignet
        commande.Longueur_Pantalon = Longueur_Pantalon
        commande.Bas = Bas

        commande.Prix_Couture = Prix_Couture
        commande.Avance = Avance
        commande.Date_Retrait_Model = Date_Retrait_Model
        #solde = float(commande.Prix_Couture ) - float(commande.Avance)
        
        commande.save()

       
        facture.Nom = Nom
        facture.Telephone = commande.Telephone
        facture.Modele_couture = Modele_Couture
        facture.Prix_Couture=int(request.POST.get("Prix_Couture"))
        facture.Avance=int(request.POST.get("Avance"))
        solde=facture.Prix_Couture - facture.Avance
        facture.Solde= solde
        facture.save()

       

        client.Nom = Nom
        client.Telephone = Telephone
        #client.Interventions = Client.Interventions
        client.save()

        messages.success(request, "Commande modifiee avec succes")
        return redirect('liste_commande')
    
    return render(request, "accounts/ModifierCommande.html")

# Suppression d'une commande

def supprimer_commande(request, commande_id):
    if request.method == "GET":

        commande = Commande.objects.get(pk = commande_id)  # Recuperer la commande correspondante
        client = Client.objects.get(Telephone = commande.Telephone)
       
        if commande.Telephone == client.Telephone:
            commande.delete() # supprimer la commande
            client.Interventions -= 1
            client.save()
            if client.Interventions == 0 :
                client.delete()
        
    messages.success(request, "Cette commande a ete bien supprimee")
    return redirect('liste_commande')

  
def profil(request, profil_id):
    if request.method == "GET":
        #commandes = Commande.objects.all()
        #clients = Client.objects.get(pk=profil_id)
        clients = Client.objects.filter(pk=profil_id)
        commandes = Commande.objects.filter(Telephone=profil_id)
        
        context ={  'clients': clients, 'commandes': commandes }
        return render (request, "accounts/Commandes_de_chaque_client.html", context=context)
    
'''def facture(request, commande_id):
    #commande = Commande.objects.filter(pk=commande_id)
    if request.method == "GET":
        commande = Commande.objects.filter(pk=commande_id)
        #facture = Facture.objects.get(command = commande_id)
        facture = Facture.objects.filter(command = commande_id )

        context = {"facture": facture, "commandes": commande}
        return render(request, "accounts/Facture.html", context)'''

def facture(request, commande_id):
    #commande = Commande.objects.filter(pk=commande_id)
    if request.method == "GET":
        commande = Commande.objects.get(pk=commande_id)
        #id = commande_id
        #facture = Facture.objects.get(command = commande_id)
        #facture = Facture.objects.filter(pk = id )
        facture = Facture.objects.get(command = commande)
        #context = {"facture": facture, "commandes": commande}
        context = {"facture" : facture, 'commande': commande}
        return render(request, "accounts/Facture.html", context)


   
def historique(request):
    today = timezone.now().date()     # on recupere la date d'aujourd'hui
    troisjoursavant = today - timedelta(days=1)  # on calcul le nombre de jours (dans notre cas, 3)

    commandes = Commande.objects.filter(Date_Depot_Model__gte=troisjoursavant)  # on filtre les commandes prises dont la uree est comprise entre 1 et 3 jours
    context = {'commandes': commandes}
    return render(request, 'accounts/Historique.html', context)

def rendezVous(request):
    maintenant = datetime.now()  # on recupere  la date et l'heure actuelle

    commandes= Commande.objects.filter(Date_Retrait_Model__gte=maintenant).order_by("Date_Retrait_Model")[:5]
    if Commande.Date_Retrait_Model == maintenant :
        commandes.delete()
    context = {'commandes': commandes}
    return render(request, 'accounts/RendezVous.html', context)

# Pour techarger facture


'''def telecharger_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    # Supposons que le champ 'fichier_facture' dans le modèle Facture contient le chemin du fichier PDF
    pdf_path = facture.fichier_facture.path
    filename = f'facture_{facture.id}.pdf'
    
    # Ouvrir le fichier PDF en tant que réponse de fichier
    response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response'''

'''
def generationPdf(request):
    #facture = Facture.objects.all() # J'appelle ma facture correspondant a l'id de la commande
    commande = Commande.objects.get(pk=commande_id)
    facture = Facture.objects.get(command = commande)
    template_path = 'accounts/Facture.html'     # Fichier html ou je veux telecharger
    context = {'facture' : facture}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = ' filename="facture_report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response '''


def generationPdf(request):
    #facture = Facture.objects.all() # J'appelle ma facture correspondant a l'id de la commande
    clients =  Client.objects.all()

    template_path = 'accounts/pdfReport.html'     # Fichier html ou je veux telecharger
    context = {'clients' : clients}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = ' filename="facture_report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


'''def facturePdf(request):
    #facture = Facture.objects.all() # J'appelle ma facture correspondant a l'id de la commande
    factures =  Facture.objects.all()
    #factures =  Facture.objects.get(pk = facture_id)

    template_path = 'accounts/FacturePdf.html'     # Fichier html ou je veux telecharger
    context = {'factures' : factures}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = ' filename="facture_report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response'''


'''def facturePdf(request, facture_id):
    #facture = Facture.objects.all() # J'appelle ma facture correspondant a l'id de la commande
    #factures =  Facture.objects.all()
    #factures =  Facture.objects.get(pk = facture_id)
    #commande = Commande.objects.get(pk=commande_id)
    facture = Facture.objects.get(pk = facture_id)
    template_path = 'accounts/FacturePdf.html'     # Fichier html ou je veux telecharger
    context = {'facture' : facture}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = ' filename="facture_report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response'''

def facturePdf(request, commande_id):
    #facture = Facture.objects.all() # J'appelle ma facture correspondant a l'id de la commande
    #factures =  Facture.objects.all()
    #factures =  Facture.objects.get(pk = facture_id)
    #commande = Commande.objects.get(pk=commande_id)
    facture = Facture.objects.get(pk = commande_id)
    template_path = 'accounts/FacturePdf.html'     # Fichier html ou je veux telecharger
    context = {'facture' : facture}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = ' filename="facture_report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


"""
def modifier_commande(request, commande_id):
    if request.method == "GET":
        commande = get_object_or_404(Commande, id=commande_id)
        #commande = Commande.objects.filter(id=commande_id)
        contex = {'commande' : commande}
       
        return render(request, 'accounts/ModifierCommande.html', contex )
    
    commande = get_object_or_404(Commande, id=commande_id)
    # partie  pour modifier

    if request.method == "POST":
        #Commande.commande_id=client ,
        Nom = request.POST.get("Nom")
        Telephone = request.POST.get("Telephone")
        #Client = request.POST.get("Client")
        Modele_Couture = request.POST.get("Modele_Couture")
        Nombre_Pagnes = request.POST.get("Nombre_Pagnes")
        Dos = request.POST.get("Dos")
        Epaule = request.POST.get("Epaule")
        Poitrine = request.POST.get("Poitrine")
        Longueur_Manche = request.POST.get("Longueur_Manche")
        Tour_Manche = request.POST.get("Tour_Manche")
        Longueur_Taille = request.POST.get("Longueur_Taille")
        Tour_Taille = request.POST.get("Tour_Taille")
        Pince_longueur_seins = request.POST.get("Pince_longueur_seins")
        Longueur_Camisole = request.POST.get("Longueur_Camisole")
        Longueur_Robe = request.POST.get("Longueur_Robe")
        Longueur_Chemise = request.POST.get("Longueur_Chemise")
        Messure_Bassin = request.POST.get("Messure_Bassin")
        Mesure_Ceinture = request.POST.get("Mesure_Ceinture")
        Mesure_Cuisse = request.POST.get("Mesure_Cuisse")
        Mesure_Genoux = request.POST.get("Mesure_Genoux")
        Longeur_Jupe = request.POST.get("Longeur_Jupe")
        Longueur_Bras = request.POST.get("Longueur_Bras")
        Longueur_Poignet = request.POST.get("Longueur_Poignet")
        Prix_Couture = request.POST.get("Prix_Couture")
        Avance = request.POST.get("Avance")


        commande.Nom = Nom
        commande.Telephone = Telephone
        #Client = request.POST.get("Client")
        commande.Modele_Couture = Modele_Couture
        commande.Nombre_Pagnes = Nombre_Pagnes
        commande.Dos = Dos
        commande.Epaule = Epaule
        commande.Poitrine = Poitrine
        commande.Longueur_Manche = Longueur_Manche
        commande.Tour_Manche = Tour_Manche
        commande.Longueur_Taille = Longueur_Taille
        commande.Tour_Taille = Tour_Taille
        commande.Pince_longueur_seins = Pince_longueur_seins
        commande.Longueur_Camisole = Longueur_Camisole
        commande.Longueur_Robe = Longueur_Robe
        commande.Longueur_Chemise = Longueur_Chemise
        commande.Messure_Bassin = Messure_Bassin
        commande.Mesure_Ceinture = Mesure_Ceinture
        commande.Mesure_Cuisse = Mesure_Cuisse
        commande.Mesure_Genoux = Mesure_Genoux
        commande.Longeur_Jupe = Longeur_Jupe
        commande.Longueur_Bras = Longueur_Bras
        commande.Longueur_Poignet = Longueur_Poignet
        commande.Prix_Couture = Prix_Couture
        commande.Avance = Avance
        commande.save()



        #facture.save()
        messages.success(request, "Commande modifiee avec succes")
        return redirect('accounts:liste_commande')
    
    return render(request, "accounts/ModifierCommande.html")
"""