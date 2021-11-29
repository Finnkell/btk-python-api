from localflavor.br import models as br_models
from django.db import models

# CREATE TABLE user_account (
#     email text NOT NULL,
#     cpf number NOT NULL,
#     password text NOT NULL,
#     name text NOT NULL,
#     phone text NOT NULL,
#     account_type int default 0,
#     PRIMARY KEY (cpf)
# );

# CREATE TABLE user_info (
#     cpf number NOT NULL,    
#     city text,
#     state text,
#     street text,
#     neighbourhood text,
#     age int,
#     PRIMARY KEY (cpf),
#     FOREIGN KEY (cpf) REFERENCES user_account(cpf)
# );

from  django.core.validators import MinValueValidator, MaxValueValidator

class UserInfo(models.Model):
    city = models.CharField(max_length=100, blank=True, default="")
    state = models.CharField(max_length=100, blank=True, default="")
    street = models.CharField(max_length=100, blank=True, default="")
    neighbourhood = models.CharField(max_length=100, blank=True, default="")
    age = models.PositiveIntegerField(default=18, blank=True, validators=[MinValueValidator(18), MaxValueValidator(100)])
    
    class Meta:
        verbose_name = 'Cadastro de Informações de Usuário'

    def __str__(self) -> str:
        return self.city

class UserAccount(models.Model):
    class AccountType(models.IntegerChoices):
        Default = 0 # Default User - Has access to not premium data
        Premium = 1 # Paid User - has acess to premium data
    
    username = models.CharField(max_length=100, blank=False)
    password = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=40, blank=False)
    email = models.CharField(max_length=100, blank=False, unique=True)
    cpf = br_models.BRCPFField(unique=True, blank=False, primary_key=True, max_length=11)
    
    user_info = models.ForeignKey(UserInfo, null=True, on_delete=models.SET_NULL, default=None)
    
    class Meta:
        verbose_name = 'Cadastro de Usuário'
        ordering = ['username']
        
    def __str__(self) -> str:
        return self.username