from django.contrib import admin
from .models import Couturier, Client, Commande,Facture

# Register your models here.

@admin.register(Couturier)
class AdminCouturier(admin.ModelAdmin):
    list_display = ("Lastname", "Firstname", "Company", "Email", "Password", "PasswordConfirm")

@admin.register(Client)
class AdminClient(admin.ModelAdmin):
    list_display = ("Nom",  "Telephone", "Interventions", "Date_Created")
    search_fields = ["Nom"]



@admin.register(Commande)
class AdminCommande(admin.ModelAdmin):
    list_display = ("id", 
                    "Nom", 
                    "Telephone", 
                    "Modele_Couture", 
                    "Nombre_Pagnes", 
                    "Dos", 
                    "Epaule", 
                    "Poitrine", 
                    "Longueur_Manche", 
                    "Tour_Manche",
                    "Longueur_Taille", 
                    "Col",
                    "Tour_Taille", 
                    "Pince_longueur_seins", 
                    "Longueur_Camisole", 
                    "Longueur_Robe", 
                    "Frappe",
                    "Longueur_Chemise", 
                    "Messure_Bassin", 
                    "Mesure_Ceinture", 
                    "Mesure_Cuisse", 
                    "Mesure_Genoux", 
                    "Longeur_Jupe", 
                    "Longueur_Poignet", 
                    "Longueur_Pantalon", 
                    "Bas" , 
                    "Prix_Couture",  
                    "Avance", 
                    "Date_Depot_Model", 
                    "Date_Retrait_Model")
    list_filter = ['Modele_Couture']    # filtrer par client
    list_per_page = 10
    search_fields = ["Modele_Couture"]

@admin.register(Facture)
class AdminFacture(admin.ModelAdmin):
    list_display = ("id", "Date", "Nom", "Telephone", "Modele_couture", "Prix_Couture", "Avance", "Solde")