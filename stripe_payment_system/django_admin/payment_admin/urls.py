from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.transactions_list, name='transactions_list'),
    path('sync-transaction/', views.sync_transaction, name='sync_transaction'),
]