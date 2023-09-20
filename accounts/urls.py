from django.urls import path
#from django.contrib.auth import views
from . import views
#from accounts.views import home, connexion
#from user import views as user_views

from django.contrib.auth import views as auth_views

#app_name = "accounts"  # ce nom sera utilise pour creer des liens dans le but d'eviter les conflits de noms

urlpatterns = [
    path('', views.home, name="home"),

    path('connexion', views.connexion, name="connexion"),
    path('inscription', views.inscription, name="inscription"),
    path('deconnexion', views.deconnexion, name="deconnexion"),
    #path('activate/<uidb64>/<token>/', views.activate, name="activate"),

    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),

    #path('reset_password/', views.PasswordResetView.as_view(), name="reset_password"), # Pour renitialiser le mot de passe
    #path('reset_password_send/', views.PasswordChangeDoneView.as_view(), name="password_reset_done"), # Envoi  le mot de passe renitialiser dans la boite mail de l'utilisateur
    #path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"), # Pour confirmer la renitialisation du mot de passe
    #path('reset_password_complete/', views.PasswordResetCompleteView.as_view(), name="password_reset_complete"), # Pour confirmer la renitialisation du mot de passe
    
    #path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"), # Pour renitialiser le mot de passe
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = "accounts/password-reset.html"), name="password_reset"), # Pour renitialiser le mot de passe
    path('password_reset_done/', auth_views.PasswordChangeDoneView.as_view(template_name = "accounts/password-reset-done.html"), name="password_reset_done"), # Envoi  le mot de passe renitialiser dans la boite mail de l'utilisateur
    path('reset/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "accounts/password-reset-confirm.html"), name="password_reset_confirm"), # Pour confirmer la renitialisation du mot de passe
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "accounts/password-reset-complete.html"), name="password_reset_complete"), # Pour confirmer la renitialisation du mot de passe
    #path('reset/<str:uidb64>/<str:token>/', views.confirmer, name="confirmer"), # Pour confirmer la renitialisation du mot de passe

    path('client/', views.client, name="client"),
    path('commande/', views.commande, name="commande"),

    path('liste_commande/', views.liste_commande, name="liste_commande"),
   # path('<int:commande_id>/', views.show, name="show"),
   # path('ajouter_commande/', views.ajouter_commande, name="ajouter_commande"),
    path('modifier_commande/<int:commande_id>/', views.modifier_commande, name="modifier_commande"),
    path('supprimer_commande/<int:commande_id>/', views.supprimer_commande, name="supprimer_commande"), # Suppression d'une commande par rapport a son id
    path('commande<int:commande_id>/', views.facture, name="facture"), # Facture d'une commande
    #path('commande<int:facture_id>/', views.facture, name="facture"), # Facture d'une commande

    #    path('profil', views.commandes_de_chaque_client, name="commandes_de_chaque_client"), # Facture d'une commande
    path('client/<int:profil_id>/', views.profil, name="profil"),
    path('historique/', views.historique, name="historique"),
    path('rendezVous/', views.rendezVous, name="rendezVous"),
    path("generationPdf/", views.generationPdf, name="generationPdf"),
    path("<int:commande_id>/", views.facturePdf, name="facturePdf"),
    #path("Facture/<int:facture_id>/", views.facturePdf, name="facturePdf"),

   # path('<int:facture_id>/', views.telecharger_facture, name='telecharger_facture'),




]