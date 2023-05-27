from django.db import models

class Consultas(models.Model):
    text = models.CharField(max_length=280, verbose_name="Consult Text")
    datetime = models.DateTimeField(auto_now_add=True)  
    urgencia = models.CharField(max_length=280, verbose_name="Retorno sobre urgência")
    valores = models.CharField(max_length=280, verbose_name="Retorno sobre Valores")
    pessoal = models.CharField(max_length=280, verbose_name="Retorno sobre Informações pessoais")
    link = models.CharField(max_length=280, verbose_name="Retorno sobre links")