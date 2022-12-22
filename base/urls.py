"""
WESLEY WONG KEE HAN
TP059618 APU3F2205CS(CYB)

Base Application URLs Definition
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('edit-profile/', views.editProfile, name="edit-profile"),
    
    path('scan/<str:pk>/', views.scan, name="scan"),
    path('new-scan/', views.newScan, name="new-scan"),
    path('update-scan/<str:pk>/', views.updateScan, name="update-scan"),
    path('delete-scan/<str:pk>/', views.deleteScan, name="delete-scan"),
    path('change-state/<str:pk>/', views.changeState, name="change-state"),

    path('library/', views.library, name="library"),
    path('new-technique/', views.newTechnique, name="new-technique"),
    path('update-technique/<str:pk>/', views.updateTechnique, name="update-technique"),
    path('delete-technique/<str:pk>/', views.deleteTechnique, name="delete-technique"),

    path('update-simulation/<str:pk>/', views.updateSimulation, name="update-simulation"),
    path('delete-scan-simulation/<str:pk>/', views.deleteScanSimulation, name="delete-scan-simulation"),
    path('delete-template-simulation/<str:pk>/', views.deleteTemplateSimulation, name="delete-template-simulation"),

    path('template/', views.template, name="template"),
    path('view-template/<str:pk>/', views.viewTemplate, name="view-template"),
    path('new-template/<str:type>/', views.newTemplate, name="new-template"),
    path('simulate-template/<str:pk>/', views.simulateTemplate, name="simulate-template"),
    path('update-template/<str:pk>/', views.updateTemplate, name="update-template"),
    path('delete-template/<str:pk>/', views.deleteTemplate, name="delete-template"),

    path('variant/<str:pk>/', views.variant, name="variant"),
    path('new-variant/<str:pk>/', views.newVariant, name="new-variant"),
    path('update-variant/<str:pk>/', views.updateVariant, name="update-variant"),
    path('delete-variant/<str:pk>/', views.deleteVariant, name="delete-variant"),

    path('update-uservariant/<str:pk>/', views.updateUserVariant, name="update-uservariant"),
    path('delete-uservariant/<str:pk>/', views.deleteUserVariant, name="delete-uservariant"),

    path('manage/', views.manage, name="manage"),

    path('apt/', views.apt, name="apt"),
    path('new-apt/', views.newAPT, name="new-apt"),
    path('update-apt/<str:pk>/', views.updateAPT, name="update-apt"),
    path('delete-apt/<str:pk>/', views.deleteAPT, name="delete-apt"),

    path('objective/', views.objective, name="objective"),
    path('new-objective/', views.newObjective, name="new-objective"),
    path('update-objective/<str:pk>/', views.updateObjective, name="update-objective"),
    path('delete-objective/<str:pk>/', views.deleteObjective, name="delete-objective"),

    path('attackTactic/', views.attackTactic, name="attackTactic"),
    path('new-attackTactic/', views.newAttackTactic, name="new-attackTactic"),
    path('update-attackTactic/<str:pk>/', views.updateAttackTactic, name="update-attackTactic"),
    path('delete-attackTactic/<str:pk>/', views.deleteAttackTactic, name="delete-attackTactic"),

    path('attackTechnique/', views.attackTechnique, name="attackTechnique"),
    path('new-attackTechnique/', views.newAttackTechnique, name="new-attackTechnique"),
    path('update-attackTechnique/<str:pk>/', views.updateAttackTechnique, name="update-attackTechnique"),
    path('delete-attackTechnique/<str:pk>/', views.deleteAttackTechnique, name="delete-attackTechnique"),

    path('attackSubTechnique/', views.attackSubTechnique, name="attackSubTechnique"),
    path('new-attackSubTechnique/', views.newAttackSubTechnique, name="new-attackSubTechnique"),
    path('update-attackSubTechnique/<str:pk>/', views.updateAttackSubTechnique, name="update-attackSubTechnique"),
    path('delete-attackSubTechnique/<str:pk>/', views.deleteAttackSubTechnique, name="delete-attackSubTechnique"),

    path('new-glob/<str:pk>/', views.newGlob, name="new-glob"),
    path('update-glob/<str:pk>/', views.updateGlob, name="update-glob"),
    path('delete-glob/<str:pk>/', views.deleteGlob, name="delete-glob"),

    path('forbidden/', views.forbidden, name="forbidden"),
]