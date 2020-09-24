from django.urls import path
from .views import *
urlpatterns = [
    path('startgame', StartNewGame.as_view(), name='startgame'),
    path('makemove', MakeMove.as_view(), name='make_moves'),
    path('getallmoves', GetAllMoves.as_view(), name='get_moves')
]