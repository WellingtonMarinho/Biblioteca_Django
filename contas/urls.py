from django.urls import path
from . import views

urlpatterns = [
    path('index_login/', views.login, name='index_login'),
    path('', views.dashboard, name='index_dashboard'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cadastrar_livro/', views.cadastrar_livro, name='cadastrar_livro'),
    path('busca/', views.busca, name='busca'),
    path('<int:livro_id>', views.ver_livro, name='ver_livro'),
    path('cadastrar_categoria/', views.cadastrar_categoria, name='cadastrar_categoria'),
    path('sobre/', views.sobre, name='sobre'),
    path('editor/<int:livro_id>', views.editor, name='editor'),
    path('excluir/<int:livro_id>', views.excluir, name='excluir'),
]
