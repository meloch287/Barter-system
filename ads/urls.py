from django.urls import path
from . import views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('create/', views.create_ad, name='create_ad'),
    path('edit/<int:ad_id>/', views.edit_ad, name='edit_ad'),
    path('delete/<int:ad_id>/', views.delete_ad, name='delete_ad'),
    path('proposal/<int:ad_id>/', views.create_proposal, name='create_proposal'),
    path('proposals/', views.proposal_list, name='proposal_list'),
    path('proposal/<int:proposal_id>/update/', views.update_proposal_status, name='update_proposal_status'),
    path('signup/', views.signup, name='signup')
]