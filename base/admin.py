"""
WESLEY WONG KEE HAN
TP059618 APU3F2205CS(CYB)

Administrator Panel
"""

from django.contrib import admin
from .models import (
    Scan, 
    Technique, 
    Simulation, 
    Objective, 
    Template, 
    APT, 
    Variant, 
    UserVariant, 
    AttackTactic, 
    AttackTechnique, 
    AttackSubTechnique, 
    Glob
)

admin.site.register(Scan)
admin.site.register(Technique)
admin.site.register(Simulation)
admin.site.register(Objective)
admin.site.register(Template)
admin.site.register(APT)
admin.site.register(Variant)
admin.site.register(UserVariant)
admin.site.register(AttackTactic)
admin.site.register(AttackTechnique)
admin.site.register(AttackSubTechnique)
admin.site.register(Glob)