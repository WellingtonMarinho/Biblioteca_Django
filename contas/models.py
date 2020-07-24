from django.db import models
from django.utils import timezone
from django import forms


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# Responsável por toda a criação do banco de dados
class Livro(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=150)
    editora = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    edicao = models.IntegerField(blank=True, null=True)
    estante = models.IntegerField(default=0)
    prateleira = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    mostrar = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class FormLivro(forms.ModelForm):
    class Meta:
        model = Livro
        exclude = ('mostrar',)


class FormCategoria(forms.ModelForm):
    class Meta:
        model = Categoria
        exclude = ('mostrar',)
