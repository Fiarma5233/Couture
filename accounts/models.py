from django.db import models
#from django.utils import timezone

# Create your models here.

class Couturier(models.Model):
    Lastname = models.CharField(max_length=30, null=True, verbose_name="Nom",)
    Firstname = models.CharField(max_length=30, null=True, verbose_name="Prenom" )
    Company = models.CharField(max_length=30, null=True, verbose_name="Nom de votre entreprise")
    Email = models.EmailField(null=True, verbose_name="Adresse mail")
    Password = models.CharField(max_length=20, null=True, verbose_name="Mot de passe")
    PasswordConfirm = models.CharField(max_length=20, null=True, verbose_name="Confirmer votre mot de passe")


    def __str__(self) -> str: # surcharge sdu string pour eviter les nominations bizares edans l'admin
        return self.Lastname

    class Meta: # cette class permet de renommer les noms en francais des models au niveau de l;administration
        verbose_name = "Couturier"
        verbose_name_plural = "Couturiers"

class Client(models.Model):
    Nom = models.CharField(max_length=20, null=True)
    #Prenom = models.CharField(max_length=20, null=True)
    #Adresse = models.CharField(max_length=20, null=True)
    Telephone = models.CharField(max_length=8)
    Interventions = models.PositiveIntegerField(default=0)
    Date_Created = models.DateTimeField(auto_now=True)


    def __str__(self) -> str: # surcharge sdu string pour eviter les nominations bizares edans l'admin
        return self.Telephone

    class Meta: # cette class permet de renommer les noms en francais des models au niveau de l;administration
        verbose_name = "Client"
        verbose_name_plural = "Clients"



class Commande(models.Model):
    '''client = models.ForeignKey(Client, on_delete=models.CASCADE)
    Nom = models.CharField(max_length=20, null=True)
    Telephone = models.CharField(max_length=8)
    Modele_Couture = models.TextField(max_length=100, null=True)
    Nombre_Pagnes = models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Dos =  models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Epaule =  models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Poitrine =  models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Longueur_Manche =  models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Tour_Manche =  models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Longueur_Taille =  models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Tour_Taille =  models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Pince_longueur_seins =  models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Longueur_Camisole =  models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Longueur_Robe =  models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Longueur_Chemise =  models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Messure_Bassin =  models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Mesure_Ceinture =  models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Mesure_Cuisse =  models.DecimalField(null=True, max_digits=100000, decimal_places=2 )
    Mesure_Genoux =  models.DecimalField(null=True, max_digits=100000, decimal_places=2)
    Longeur_Jupe =  models.DecimalField(null=True, max_digits=100000, decimal_places=2)
    Longueur_Bras =  models.DecimalField(null=True, max_digits=100000, decimal_places=2)
    Longueur_Poignet =  models.DecimalField(null=True, max_digits=100000, decimal_places=2)
    Prix_Couture = models.PositiveBigIntegerField()
    Avance = models.PositiveBigIntegerField()
    Date_Depot_Model = models.DateTimeField(auto_now=True)
    Date_Retrait_Model = models.DateTimeField()'''


    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    Nom = models.CharField(max_length=20, null=True)
    Telephone = models.CharField(max_length=8)
    Modele_Couture = models.TextField(max_length=100, null=True)
    Nombre_Pagnes = models.IntegerField(default=0)
    Epaule =  models.IntegerField(default=0)
    Dos =  models.IntegerField(default=0)
    Poitrine =  models.IntegerField(default=0)
    Longueur_Manche =  models.IntegerField(default=0)
    Tour_Manche =  models.IntegerField(default=0)
    Longueur_Taille =  models.IntegerField(default=0)

    Col =  models.IntegerField(default=0)

    Tour_Taille =  models.IntegerField(default=0)
    Pince_longueur_seins =  models.IntegerField(default=0)
    Longueur_Camisole =  models.IntegerField(default=0)
    Longueur_Robe =  models.IntegerField(default=0)

    Frappe =  models.IntegerField(default=0)

    Longueur_Chemise =  models.IntegerField(default=0)
    Messure_Bassin =  models.IntegerField(default=0)
    Mesure_Ceinture =  models.IntegerField(default=0)
    Mesure_Cuisse =  models.IntegerField(default=0)
    Mesure_Genoux =  models.IntegerField(default=0)
    Longeur_Jupe =  models.IntegerField(default=0)
    #Longueur_Bras =  models.DecimalField(null=True, max_digits=100000, decimal_places=2)
    Longueur_Poignet =  models.IntegerField(default=0)

    Longueur_Pantalon =  models.IntegerField(default=0)

    Bas =  models.IntegerField(default=0)


    Prix_Couture = models.PositiveBigIntegerField()
    Avance = models.PositiveBigIntegerField()
    Date_Depot_Model = models.DateTimeField(auto_now=True)
    Date_Retrait_Model = models.DateField()






class Facture(models.Model):
    command=models.ForeignKey(Commande, on_delete=models.CASCADE)
    Date = models.DateTimeField(auto_now=True)
    Nom = models.CharField(max_length=60)
    Telephone = models.CharField(max_length=8, unique=False)
    Modele_couture = models.CharField(max_length=100)
    Prix_Couture = models.PositiveBigIntegerField()
    Avance = models.PositiveBigIntegerField()
    Solde = models.PositiveBigIntegerField(default=0)
    


    def __str__(self) -> str:
        return self.Nom
    
    class Meta:
        verbose_name =  'Facture'
        verbose_name_plural = "Factures"