"""
WESLEY WONG KEE HAN
TP059618 APU3F2205CS(CYB)

Django Models for Database Class
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL

class Scan(models.Model):
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, verbose_name = u'Owner')
    name = models.CharField(max_length=200, default="New Scan")
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = (
    ("STOPPED", "STOPPED"),
    ("COMPLETED", "COMPLETED"),
    ("RUNNING", "RUNNING"))

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='STOPPED')
    ip = models.CharField("IP Address", max_length=15, default="127.0.0.1")
    username = models.CharField("Machine Username", max_length=30, default="admin")
    password = models.CharField("Machine Password", max_length=50, default="admin")
    task = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = 'Scan'

    def __str__(self):
        return self.name

class Objective(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Objective'

    def __str__(self):
        return self.name

class APT(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'APT Group'

    def __str__(self):
        return self.name

class Technique(models.Model):
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, verbose_name = u'Owner')
    name = models.CharField(max_length=200, default="New Binary")
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    Objective = models.ManyToManyField(Objective, verbose_name = u'Objectives')
    APT = models.ManyToManyField(APT, blank=True, verbose_name = u'APT Groups')

    class Meta:
        verbose_name = 'LOLBin'

    def __str__(self):
        return self.name

class Template(models.Model):
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, verbose_name = u'Owner')
    name = models.CharField(max_length=200, default="New Template")
    description = models.TextField(max_length=100, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)

    # Null = True to disassociate Template from Scan after clone
    Scan = models.ForeignKey(Scan, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = 'Template'

    def __str__(self):
        return self.name

class AttackTactic(models.Model):
    name = models.CharField(max_length=20, default="New ATT&CK Tactic")
    attackid = models.CharField("ATT&CK ID", max_length=6, default="TA0000")

    class Meta:
        verbose_name = 'ATT&CK Tactic'

    def __str__(self):
        return self.name

class AttackTechnique(models.Model):
    name = models.CharField(max_length=50, default="New ATT&CK Technique")
    attackid = models.CharField("ATT&CK ID", max_length=5, default="T0000")
    AttackTactic = models.ForeignKey(AttackTactic, on_delete=SET_NULL, null=True, verbose_name = u'Parent Tactic')

    class Meta:
        verbose_name = 'ATT&CK Technique'

    def __str__(self):
        return self.name

class AttackSubTechnique(models.Model):
    name = models.CharField(max_length=50, default="New ATT&CK Sub-Technique")
    attackid = models.CharField("ATT&CK ID", max_length=4, default=".000")
    AttackTechnique = models.ForeignKey(AttackTechnique, on_delete=SET_NULL, null=True, verbose_name = u'Parent Technique')

    class Meta:
        verbose_name = 'ATT&CK Sub-Technique'

    def __str__(self):
        return self.name

class Variant(models.Model):
    name = models.CharField(max_length=200, default="New Variant")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    RISK = (
    ("HIGH", "HIGH"),
    ("MEDIUM", "MEDIUM"),
    ("LOW", "LOW"))

    severity = models.CharField(max_length=6, choices=RISK)
    Technique = models.ForeignKey(Technique, on_delete=CASCADE, null=True, verbose_name = u'Binary Used')
    AttackSubTechnique = models.ForeignKey(AttackSubTechnique, on_delete=SET_NULL, null=True, verbose_name = u'ATT&CK Sub-Technique')
    Objective = models.ForeignKey(Objective, on_delete=SET_NULL, null=True)

    payload = models.TextField("Generic Payload", default=None)
    defaultPayload = models.TextField("Default Payload", default=None)
    cleanup = models.TextField("Generic Cleanup", null=True, blank=True)
    defaultCleanup = models.TextField("Default Cleanup", null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    detection = models.TextField("Detection Guide", null=True, blank=True)
    prevention = models.TextField("Prevention Guide", null=True, blank=True)
    mitre = models.TextField("MITRE ATT&CK", null=True, blank=True)
    lolbas = models.TextField("LOLBAS Project", null=True, blank=True)

    class Meta:
        verbose_name = 'Variant'

    def __str__(self):
        return str(self.id) + ": " + self.name

class UserVariant(models.Model):
    Variant = models.ForeignKey(Variant, on_delete=CASCADE, null=True)
    name = models.CharField(max_length=200, default="Custom Variant")
    payload = models.TextField(default=None)
    cleanup = models.TextField(null=True, blank=True)
    detected = models.BooleanField(null=True, blank=True)

    CHOICES = (
    ("Yes", "Yes"),
    ("No", "No"))

    chainPrevious = models.CharField("Chain To Previous", max_length=3, choices=CHOICES, default='No')
    highIntegrity = models.CharField("High Integrity Process", max_length=3, choices=CHOICES, default='No')

    class Meta:
        ordering = ['id']
        verbose_name = 'Custom Variant'

    def __str__(self):
        return str(self.name)

class Simulation(models.Model):
    name = models.CharField(max_length=200, default="New Simulation")
    UserVariant = models.ManyToManyField(UserVariant, blank=True)

    # Scan can be null for Template
    Scan = models.ForeignKey(Scan, on_delete=CASCADE, null=True, blank=True)

    # Template can be null for Scans
    Template = models.ForeignKey(Template, on_delete=CASCADE, null=True, blank=True)    

    class Meta:
        verbose_name = 'Simulation'

    def __str__(self):
        return self.name

class Glob(models.Model):
    name = models.CharField(max_length=200, default=None)
    Technique = models.ForeignKey(Technique, on_delete=CASCADE, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Globfuscation'

    def __str__(self):
        return self.name