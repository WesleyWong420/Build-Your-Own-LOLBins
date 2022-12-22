"""
WESLEY WONG KEE HAN
TP059618 APU3F2205CS(CYB)

Model Form
"""

from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import (
    Scan, 
    Technique, 
    Template, 
    Simulation, 
    Variant, 
    UserVariant, 
    APT, 
    Objective, 
    AttackTactic, 
    AttackTechnique, 
    AttackSubTechnique, 
    Glob
)

class ScanForm(ModelForm):
    class Meta:
        model = Scan
        fields = '__all__'
        exclude = ['user', 'status', 'task']

class TechniqueForm(ModelForm):
    class Meta:
        model = Technique
        fields = '__all__'
        exclude = ['user']

class TemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = '__all__'
        exclude = ['user', 'public', 'Simulation']

class TemplateUpdateForm(ModelForm):
    class Meta:
        model = Template
        fields = '__all__'
        exclude = ['user', 'public', 'Scan', 'Simulation']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class SimulationForm(ModelForm):
    class Meta:
        model = Simulation
        fields = '__all__'
        exclude = ['Scan', 'Template']

class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = '__all__'
        exclude = ['Technique']

class UserVariantForm(ModelForm):
    class Meta:
        model = UserVariant
        fields = '__all__'
        exclude = ['Variant', 'detected']

class APTForm(ModelForm):
    class Meta:
        model = APT
        fields = '__all__'

class ObjectiveForm(ModelForm):
    class Meta:
        model = Objective
        fields = '__all__'

class AttackTacticForm(ModelForm):
    class Meta:
        model = AttackTactic
        fields = '__all__'

class AttackTechniqueForm(ModelForm):
    class Meta:
        model = AttackTechnique
        fields = '__all__'

class AttackSubTechniqueForm(ModelForm):
    class Meta:
        model = AttackSubTechnique
        fields = '__all__'

class GlobForm(ModelForm):
    class Meta:
        model = Glob
        fields = '__all__'
        exclude = ['Technique']