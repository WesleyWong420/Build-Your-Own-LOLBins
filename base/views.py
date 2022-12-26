"""
WESLEY WONG KEE HAN
TP059618 APU3F2205CS(CYB)

Views Handler for the Base Application
"""

from django.shortcuts import render, redirect
from django.db.models import Q, Count, Value
from django.db.models.functions import Concat
from django.contrib import messages
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .utilities import *
import xlwt
import json
from .tasks import *
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
from .forms import (
    ScanForm, 
    TechniqueForm, 
    TemplateForm, 
    TemplateUpdateForm, 
    UserForm, 
    SimulationForm, 
    VariantForm, 
    UserVariantForm, 
    APTForm, 
    ObjectiveForm, 
    AttackTacticForm, 
    AttackTechniqueForm, 
    AttackSubTechniqueForm, 
    GlobForm, 
)

def loginPage(request):
    page = 'login' 
    context = {'page': page} 

    # Redirect authenticated user to home page when they browse to /login URI manually
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Empty fields
        if username == "" or password == "":
            messages.error(request, "Please fill in all the fields!")
            return render(request, 'base/authentication.html', context)

        # User does not exists
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exists!")
            return render(request, 'base/authentication.html', context)

        user = authenticate(request, username=username, password=password)

        # Password incorrect
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect!')

    return render(request, 'base/authentication.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            login(request, user)
    
            return redirect('home')

        elif form.errors:
            
            # Filtering based on results of Django back-end validation
            for field in form:
                if strip_tags(field.errors) == "This field is required.":
                    messages.error(request, 'Username is required!')
                    break
                elif strip_tags(field.errors) == "A user with that username already exists.":
                    messages.error(request, 'The user already exists!')
                    break
                else:
                    for error in field.errors:
                        if strip_tags(error) == 'The two password fields didn’t match.':
                            messages.error(request, 'Passwords do not match!')
                            break
                        else:
                            messages.error(request, 'Password cannot be less than 8 characters, entirely numeric, common passwords or too similar to the username!')
                            break

    context = {'form': form}
    return render(request, 'base/authentication.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    userScans = Scan.objects.filter(user=user).order_by('-created')  

    context = {'user': user, 'userScans': userScans}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def editProfile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/editProfile.html', {'form': form})

def home(request):
    scans = Scan.objects.all().order_by('-updated')
    techniques = Technique.objects.all().order_by('-created')

    if request.user.is_authenticated:
        userScans = Scan.objects.filter(user=request.user).order_by('-created')
        scan_count = userScans.count()
        context = {'scans': scans, 'techniques': techniques, 'scan_count':scan_count, 'userScans': userScans}
    else:
        context = {'scans': scans, 'techniques': techniques}

    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def scan(request, pk):
    currentScan = Scan.objects.get(id=pk)
    
    simulations = currentScan.simulation_set.all()

    variants = Variant.objects.all()
    variant_count = variants.count()

    if request.user != currentScan.user and request.user.is_superuser != 1:
        return redirect('forbidden')   

    # Create/Add Simulations on Scan page
    if request.method == "POST":
        simulation = Simulation.objects.create(
            name = request.POST.get('name'),
            Scan = currentScan,
            Template = None)

        simulation.save()

        return redirect('scan', pk=currentScan.id)

    context = {'scan': currentScan, 'simulations': simulations, 'variants': variants, 'variant_count': variant_count}
    return render(request, 'base/scan.html', context)

@login_required(login_url='login')
def newScan(request):
    form = ScanForm()

    if request.method == 'POST':
        form = ScanForm(request.POST)

        if form.is_valid():
            scan = form.save(commit=False)
            scan.user = request.user    
            scan.save()
            messages.success(request, 'Scan created successfully!')
            return redirect('scan', pk=scan.id)

    context = {'form': form}
    return render(request, 'base/newScan.html', context)

@login_required(login_url='login')
def updateScan(request, pk):
    scan = Scan.objects.get(id=pk)
    form = ScanForm(instance=scan)

    if request.user != scan.user and request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        form = ScanForm(request.POST, instance=scan)

        if form.is_valid():
            form.save()
            messages.success(request, 'Scan updated successfully!')
            return redirect('scan', pk=scan.id)

    context = {'form': form}
    return render(request, 'base/updateScan.html', context)

@login_required(login_url='login')
def deleteScan(request, pk):
    scan = Scan.objects.get(id=pk)

    if request.user != scan.user and request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        for simulation in scan.simulation_set.all():
            for userVariant in simulation.UserVariant.all():
                userVariant.delete()
        scan.delete()
        messages.success(request, 'Scan deleted successfully!')
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': scan})

@login_required(login_url='login')
def changeState(request, pk):
    scan = Scan.objects.get(id=pk)

    if request.user != scan.user and request.user.is_superuser != 1:
        return redirect('forbidden')  

    if scan.status == 'STOPPED' or scan.status == 'COMPLETED' or scan.status == 'ERROR':
        scan.status = 'RUNNING'
        scan.save()

        for simulation in scan.simulation_set.all():
            for userVariant in simulation.UserVariant.all():
                userVariant.detected = None
                userVariant.save()

        messages.success(request, 'Scan started successfully!')
        scan.task = RunScan.delay(pk)
        scan.save()
    elif scan.status == 'RUNNING':
        task = RunScan.AsyncResult(scan.task)
        task.abort()

        scan.status = 'STOPPED'
        scan.save()

        for simulation in scan.simulation_set.all():
            for userVariant in simulation.UserVariant.all():
                userVariant.detected = None
                userVariant.save()

        messages.success(request, 'Scan stopped successfully!')

    return redirect('scan', pk=scan.id)

def library(request):
    fullTechniques = Technique.objects.all().distinct()
    objectives = Objective.objects.annotate(count=Count('technique')).order_by('-count')
    groups = APT.objects.annotate(count=Count('technique')).order_by('-count')
    variants = Variant.objects.all()

    q = request.GET.get('q') if request.GET.get('q') != None else '' 

    techniques = Technique.objects.filter(
        Q(name__icontains=q) | 
        Q(Objective__name__icontains=q) |
        Q(APT__name__icontains=q)).order_by('-updated').distinct()

    context = {'objectives': objectives, 'techniques': techniques, 'fullTechniques': fullTechniques, 'groups': groups, 'variants': variants}
    return render(request, 'base/library.html', context)

@login_required(login_url='login')
def newTechnique(request):
    form = TechniqueForm()
    objectives = Objective.objects.all()
    groups = APT.objects.all()

    if request.user.is_superuser != 1:
        return redirect('forbidden')

    if request.method == 'POST':

        technique = Technique.objects.create(
            user = request.user,
            name = request.POST.get('name'),
            description = request.POST.get('description'))

        # Retrieve from <select> template
        objective_name = request.POST.getlist('objective_name')

        # Iterate list and append objectives to ManyToMany field of Technique
        for item in objective_name:
            objective = Objective.objects.get(name=item)
            technique.Objective.add(objective)

        # Retrieve from <select> template
        group_name = request.POST.getlist('group_name')

        # Iterate list and append APT to ManyToMany field of Technique
        for item in group_name:
            group = APT.objects.get(name=item)
            technique.APT.add(group)

        messages.success(request, 'Technique created successfully!')

        return redirect('library')

    context = {'form': form, 'objectives': objectives, 'groups': groups}
    return render(request, 'base/newTechnique.html', context)

@login_required(login_url='login')
def updateTechnique(request, pk):
    technique = Technique.objects.get(id=pk)
    form = TechniqueForm(instance=technique)
    objectives = Objective.objects.all()

    if request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        form = TechniqueForm(request.POST, instance=technique)

        technique.user = request.user
        technique.name = request.POST.get('name')
        technique.description = request.POST.get('description')

        # Reset list and re-populate
        empty_list = []
        technique.Objective.set(empty_list)
        objective_name = request.POST.getlist('objective_name')

        # Iterate list and append objectives to ManyToMany field of Technique
        for item in objective_name:
            objective = Objective.objects.get(id=item)
            technique.Objective.add(objective)

        # Reset list and re-populate
        technique.APT.set(empty_list)
        group_name = request.POST.getlist('group_name')

        # Iterate list and append APT to ManyToMany field of Technique
        for item in group_name:
            group = APT.objects.get(id=item)
            technique.APT.add(group)

        technique.save()
        messages.success(request, 'Technique updated successfully!')

        return redirect('library')

    context = {'form': form, 'objectives': objectives, 'technique': technique}
    return render(request, 'base/updateTechnique.html', context)

@login_required(login_url='login')
def deleteTechnique(request, pk):
    technique = Technique.objects.get(id=pk)

    if request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        technique.delete()
        messages.success(request, 'Technique deleted successfully!')
        return redirect('library')

    return render(request, 'base/delete.html', {'obj': technique})

@login_required(login_url='login')
def updateSimulation(request, pk):
    simulation = Simulation.objects.get(id=pk)
    form = SimulationForm(instance=simulation)
    variants = Variant.objects.all()

    if simulation.Template == None:
        if request.user != simulation.Scan.user and request.user.is_superuser != 1:
            return redirect('forbidden')   
    else:
        if request.user != simulation.Template.user and request.user.is_superuser != 1:
            return redirect('forbidden')  

    if request.method == 'POST':
        form = SimulationForm(request.POST, instance=simulation)

        simulation.name = request.POST.get('name')

        # Get selection (variant to add) from submission form
        variant_name = request.POST.getlist('variant_name')

        for item in variant_name:
            variant = Variant.objects.get(id=item)
            userVariant = UserVariant.objects.create(Variant=variant, name=variant.name, payload=variant.defaultPayload, cleanup=variant.defaultCleanup, detected = None, chainPrevious = 'No', highIntegrity = 'No')
            simulation.UserVariant.add(userVariant)

        simulation.save()
        messages.success(request, 'Simulation updated successfully!')

        if simulation.Template == None:
            return redirect('scan', pk=simulation.Scan.id)
        else:
            return redirect('view-template', pk=simulation.Template.id)

    context = {'form': form, 'variants': variants, 'simulation': simulation}
    return render(request, 'base/updateSimulation.html', context)

@login_required(login_url='login')
def deleteScanSimulation(request, pk):
    simulation = Simulation.objects.get(id=pk)

    if request.user != simulation.Scan.user and request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        for userVariant in simulation.UserVariant.all():
            userVariant.delete()
        simulation.delete()
        simulation.Scan.save()
        messages.success(request, 'Simulation deleted successfully!')
        return redirect('scan', pk=simulation.Scan.id)

    return render(request, 'base/delete.html', {'obj': simulation})

@login_required(login_url='login')
def deleteTemplateSimulation(request, pk):
    simulation = Simulation.objects.get(id=pk)

    if request.user != simulation.Template.user and request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        for userVariant in simulation.UserVariant.all():
            userVariant.delete()
        simulation.delete()
        simulation.Template.save()
        messages.success(request, 'Simulation deleted successfully!')
        return redirect('view-template', pk=simulation.Template.id)

    return render(request, 'base/delete.html', {'obj': simulation})

def template(request):
    templates = Template.objects.all().order_by('-created')

    superusers = User.objects.filter(is_superuser=True).values('username')
    template_apt = Template.objects.filter(user__username__in=superusers, public=True).order_by('-created')
    template_apt_count = template_apt.count()

    template_community = Template.objects.filter(
    public=True).exclude(user__username__in=superusers).order_by('-created')
    template_community_count = template_community.count()

    context = {'templates': templates,
    'template_apt': template_apt, 'template_apt_count': template_apt_count,
    'template_community': template_community, 'template_community_count': template_community_count}

    if request.user.is_authenticated:
        template_self = Template.objects.filter(
        Q(user=request.user) & 
        Q(public=False)).order_by('-created')
        template_self_count = template_self.count()

        # Add additional context to dictionary
        context['template_self'] =  template_self
        context['template_self_count'] = template_self_count

    return render(request, 'base/template.html', context)

@login_required(login_url='login')
def viewTemplate(request, pk):
    currentTemplate = Template.objects.get(id=pk)
    
    simulations = Simulation.objects.all()

    variants = Variant.objects.all()
    variant_count = variants.count() 

    if currentTemplate.public == False and request.user != currentTemplate.user:
        return redirect('forbidden')  

    # Create/Add Simulations on Template page
    if request.method == "POST":
        simulation = Simulation.objects.create(
            name = request.POST.get('name'),
            Scan = None,
            Template = currentTemplate)

        simulation.save()

        return redirect('view-template', pk=pk)

    context = {'template': currentTemplate, 'simulations': simulations, 'variants': variants, 'variant_count': variant_count}
    return render(request, 'base/viewTemplate.html', context)

@login_required(login_url='login')
def newTemplate(request, type):
    # Limit users to create template from their own scans only
    form = TemplateForm()
    form.fields["Scan"].queryset = Scan.objects.filter(user=request.user)

    if type == "apt" and request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        form = TemplateForm(request.POST)

        if form.is_valid():
            template = form.save(commit=False)
            template.user = request.user

            if type == "apt" or type == "community":
                template.public = True
            else:
                template.public = False

            # Disassociate to prevent CASCADE DELETE
            template.Scan = None
            template.save()

            # Retrieve the Scan ID that is used to create this template
            currentScan = Scan.objects.get(pk=request.POST.get('Scan'))

            for oldSimulation in currentScan.simulation_set.all():
                # Dereference Scan pointer for Simulation
                # Fix Template pointer for Simulation
                simulation = Simulation.objects.create(name=oldSimulation.name, Scan=None, Template=template)
                simulation.save()

                # Retrieve all user variants of the simulation from target scan
                variant_list = oldSimulation.UserVariant.values_list('id', flat=True)
            
                # Iterate list and append variants to ManyToMany field of Simulation
                for variant_id in variant_list:
                    oldVariant = UserVariant.objects.get(pk=variant_id)
                    userVariant = UserVariant.objects.create(Variant=oldVariant.Variant, name=oldVariant.name, payload=oldVariant.payload, cleanup=oldVariant.cleanup, detected = None, chainPrevious = oldVariant.chainPrevious, highIntegrity = oldVariant.highIntegrity)
                    simulation.UserVariant.add(userVariant)
                    simulation.save()

            messages.success(request, 'Template created successfully!')
            return redirect('template')

    context = {'form': form}
    return render(request, 'base/newTemplate.html', context)

@login_required(login_url='login')
def simulateTemplate(request, pk):
    fromTemplate = True
    currentTemplate = Template.objects.get(id=pk)   

    if currentTemplate.public == False and request.user != currentTemplate.user:
        return redirect('forbidden')  

    form = ScanForm()

    if request.method == 'POST':
        form = ScanForm(request.POST)

        if form.is_valid():
            scan = form.save(commit=False)
            scan.user = request.user    
            scan.save()

            # Do the opposite for Scan -> Template process
            for oldSimulation in currentTemplate.simulation_set.all():
                # Dereference Template pointer for Simulation
                # Fix Scan pointer for Simulation
                simulation = Simulation.objects.create(name=oldSimulation.name, Scan=scan, Template=None)
                simulation.save()

                # Retrieve all variants of the simulation from target scan
                variant_list = oldSimulation.UserVariant.values_list('id', flat=True)
            
                # Iterate list and append variants to ManyToMany field of Simulation
                for variant_id in variant_list:
                    oldVariant = UserVariant.objects.get(pk=variant_id)
                    userVariant = UserVariant.objects.create(Variant=oldVariant.Variant, name=oldVariant.name, payload=oldVariant.payload, cleanup=oldVariant.cleanup, detected = None, chainPrevious = oldVariant.chainPrevious, highIntegrity = oldVariant.highIntegrity)
                    simulation.UserVariant.add(userVariant)
                    simulation.save()

            messages.success(request, 'Scan created successfully!')
            return redirect('scan', pk=scan.id)

    context = {'form': form, 'fromTemplate': fromTemplate, 'template': currentTemplate}
    return render(request, 'base/newScan.html', context)

@login_required(login_url='login')
def updateTemplate(request, pk):
    template = Template.objects.get(id=pk)
    form = TemplateUpdateForm(instance=template)

    if request.user != template.user and request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        form = TemplateUpdateForm(request.POST, instance=template)

        if form.is_valid():
            form.save()
            messages.success(request, 'Scan updated successfully!')
            return redirect('view-template', pk=template.id)

    context = {'form': form}
    return render(request, 'base/updateTemplate.html', context)

@login_required(login_url='login')
def deleteTemplate(request, pk):
    template = Template.objects.get(id=pk)

    if request.user != template.user and request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        for simulation in template.simulation_set.all():
            for userVariant in simulation.UserVariant.all():
                userVariant.delete()
        template.delete()
        messages.success(request, 'Template deleted successfully!')
        return redirect('template')

    return render(request, 'base/delete.html', {'obj': template})

def variant(request, pk):
    technique = Technique.objects.get(id=pk)
    
    variants = technique.variant_set.all()
    variant_count = variants.count()

    globs  = technique.glob_set.all()
    glob_count = globs.count()

    context = {'technique': technique, 'variants': variants, 'variant_count': variant_count, 'globs': globs, 'glob_count': glob_count}
    return render(request, 'base/variant.html', context)

@login_required(login_url='login')
def newVariant(request, pk):
    technique = Technique.objects.get(id=pk)
    form = VariantForm()

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    if request.method == 'POST':
        form = VariantForm(request.POST)

        if form.is_valid():
            variant = form.save(commit=False)
            variant.Technique = technique    
            variant.save()
            messages.success(request, 'Variant created successfully!')
            return redirect('variant', pk=variant.Technique.id)

    context = {'form': form, 'technique': technique}
    return render(request, 'base/newVariant.html', context)

@login_required(login_url='login')
def updateVariant(request, pk):
    variant = Variant.objects.get(id=pk)
    form = VariantForm(instance=variant)

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    if request.method == 'POST':
        form = VariantForm(request.POST, instance=variant)

        if form.is_valid():
            form.save()
            messages.success(request, 'Variant updated successfully!')

            return redirect('variant', pk=variant.Technique.id)

    context = {'form': form}
    return render(request, 'base/updateVariant.html', context)

@login_required(login_url='login')
def deleteVariant(request, pk):
    variant = Variant.objects.get(id=pk)

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    if request.method == 'POST':
        variant.delete()
        messages.success(request, 'Variant deleted successfully!')

        return redirect('variant', pk=variant.Technique.id)

    return render(request, 'base/delete.html', {'obj': variant})

@login_required(login_url='login')
def updateUserVariant(request, pk):
    userVariant = UserVariant.objects.get(id=pk)
    form = UserVariantForm(instance=userVariant)
    simulation = userVariant.simulation_set.all()[0]

    if simulation.Template == None:
        if request.user != simulation.Scan.user and request.user.is_superuser != 1:
            return redirect('forbidden') 
    else:
        if request.user != simulation.Template.user and request.user.is_superuser != 1:
            return redirect('forbidden') 

    if request.method == 'POST':
        form = UserVariantForm(request.POST, instance=userVariant)

        if form.is_valid():
            form.save()
            messages.success(request, 'Details updated successfully!')

            if simulation.Template == None:
                return redirect('scan', pk=simulation.Scan.id)
            else:
                return redirect('view-template', pk=simulation.Template.id)

    context = {'form': form}
    return render(request, 'base/updateUserVariant.html', context)

@login_required(login_url='login')
def deleteUserVariant(request, pk):
    userVariant = UserVariant.objects.get(id=pk)
    simulation = userVariant.simulation_set.all()[0]

    if simulation.Template == None:
        if request.user != simulation.Scan.user and request.user.is_superuser != 1:
            return redirect('forbidden') 
    else:
        if request.user != simulation.Template.user and request.user.is_superuser != 1:
            return redirect('forbidden') 

    if request.method == 'POST':
        userVariant.delete()
        messages.success(request, 'Details deleted successfully!')

        if simulation.Template == None:
            return redirect('scan', pk=simulation.Scan.id)
        else:
            return redirect('view-template', pk=simulation.Template.id)

    return render(request, 'base/delete.html', {'obj': userVariant})

@login_required(login_url='login')
def manage(request):
    apts = APT.objects.all()
    apt_count = apts.count()

    objectives = Objective.objects.all()
    objective_count = objectives.count()

    attackTactics = AttackTactic.objects.all()
    attackTechniques = AttackTechnique.objects.all()
    attackSubTechniques = AttackSubTechnique.objects.exclude(attackid=".000")
    ttp_count = attackTactics.count() + attackTechniques.count() + attackSubTechniques.count()

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    context = {'apts': apts, 'apt_count': apt_count, 'objectives': objectives, 'objective_count': objective_count, 'attackTactics': attackTactics, 'attackTechniques': attackTechniques, 'attackSubTechniques': attackSubTechniques, 'ttp_count': ttp_count}
    return render(request, 'base/manage.html', context)

@login_required(login_url='login')
def apt(request):
    apts = APT.objects.all()
    apt_count = apts.count()

    objectives = Objective.objects.all()
    objective_count = objectives.count()

    attackTactics = AttackTactic.objects.all()
    attackTechniques = AttackTechnique.objects.all()
    attackSubTechniques = AttackSubTechnique.objects.exclude(attackid=".000")
    ttp_count = attackTactics.count() + attackTechniques.count() + attackSubTechniques.count()

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    context = {'apts': apts, 'apt_count': apt_count, 'objective_count': objective_count, 'ttp_count': ttp_count}
    return render(request, 'base/apt.html', context)

@login_required(login_url='login')
def newAPT(request):
    form = APTForm()

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    if request.method == 'POST':
        form = APTForm(request.POST)

        if form.is_valid():
            apt = form.save(commit=False) 
            apt.save()
            messages.success(request, 'APT Group created successfully!')
            return redirect('apt')

    context = {'form': form}
    return render(request, 'base/newAPT.html', context)

@login_required(login_url='login')
def updateAPT(request, pk):
    apt = APT.objects.get(id=pk)
    form = APTForm(instance=apt)

    if request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        form = APTForm(request.POST, instance=apt)

        if form.is_valid():
            form.save()
            messages.success(request, 'APT Group updated successfully!')
            return redirect('apt')
    
    context = {'form': form}
    return render(request, 'base/updateAPT.html', context)

@login_required(login_url='login')
def deleteAPT(request, pk):
    apt = APT.objects.get(id=pk)

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    if request.method == 'POST':
        apt.delete()
        messages.success(request, 'APT Group deleted successfully!')

        return redirect('apt')

    return render(request, 'base/delete.html', {'obj': apt})

@login_required(login_url='login')
def objective(request):
    apts = APT.objects.all()
    apt_count = apts.count()

    objectives = Objective.objects.all()
    objective_count = objectives.count()

    attackTactics = AttackTactic.objects.all()
    attackTechniques = AttackTechnique.objects.all()
    attackSubTechniques = AttackSubTechnique.objects.exclude(attackid=".000")
    ttp_count = attackTactics.count() + attackTechniques.count() + attackSubTechniques.count()

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    context = {'objectives': objectives, 'apt_count': apt_count, 'objective_count': objective_count, 'ttp_count': ttp_count}
    return render(request, 'base/objective.html', context)

@login_required(login_url='login')
def newObjective(request):
    form = ObjectiveForm()

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    if request.method == 'POST':
        form = ObjectiveForm(request.POST)

        if form.is_valid():
            objective = form.save(commit=False) 
            objective.save()
            messages.success(request, 'Objective created successfully!')
            return redirect('objective')

    context = {'form': form}
    return render(request, 'base/newObjective.html', context)

@login_required(login_url='login')
def updateObjective(request, pk):
    objective = Objective.objects.get(id=pk)
    form = ObjectiveForm(instance=objective)

    if request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        form = ObjectiveForm(request.POST, instance=objective)

        if form.is_valid():
            form.save()
            messages.success(request, 'Objective updated successfully!')
            return redirect('objective')
    
    context = {'form': form}
    return render(request, 'base/updateObjective.html', context)

@login_required(login_url='login')
def deleteObjective(request, pk):
    objective = Objective.objects.get(id=pk)

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    if request.method == 'POST':
        objective.delete()
        messages.success(request, 'Objective deleted successfully!')

        return redirect('objective')

    return render(request, 'base/delete.html', {'obj': objective})

@login_required(login_url='login')
def attackTactic(request):
    apts = APT.objects.all()
    apt_count = apts.count()

    objectives = Objective.objects.all()
    objective_count = objectives.count()

    attackTactics = AttackTactic.objects.all()
    attackTechniques = AttackTechnique.objects.all()
    attackSubTechniques = AttackSubTechnique.objects.exclude(attackid=".000")
    ttp_count = attackTactics.count() + attackTechniques.count() + attackSubTechniques.count()

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    context = {'attackTactics': attackTactics, 'apt_count': apt_count, 'objective_count': objective_count, 'ttp_count': ttp_count}
    return render(request, 'base/attackTactic.html', context)

@login_required(login_url='login')
def newAttackTactic(request):
    form = AttackTacticForm()

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    if request.method == 'POST':
        form = AttackTacticForm(request.POST)

        if form.is_valid():
            attackTactic = form.save(commit=False) 
            attackTactic.save()
            messages.success(request, 'Tactic created successfully!')
            return redirect('attackTactic')

    context = {'form': form}
    return render(request, 'base/newAttackTactic.html', context)

@login_required(login_url='login')
def updateAttackTactic(request, pk):
    attackTactic = AttackTactic.objects.get(id=pk)
    form = AttackTacticForm(instance=attackTactic)

    if request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        form = AttackTacticForm(request.POST, instance=attackTactic)

        if form.is_valid():
            form.save()
            messages.success(request, 'Tactic updated successfully!')
            return redirect('attackTactic')
    
    context = {'form': form}
    return render(request, 'base/updateAttackTactic.html', context)

@login_required(login_url='login')
def deleteAttackTactic(request, pk):
    attackTactic = AttackTactic.objects.get(id=pk)

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    if request.method == 'POST':
        attackTactic.delete()
        messages.success(request, 'Tactic deleted successfully!')

        return redirect('attackTactic')

    return render(request, 'base/delete.html', {'obj': attackTactic})

@login_required(login_url='login')
def attackTechnique(request):
    apts = APT.objects.all()
    apt_count = apts.count()

    objectives = Objective.objects.all()
    objective_count = objectives.count()

    attackTactics = AttackTactic.objects.all()
    attackTechniques = AttackTechnique.objects.all()
    attackSubTechniques = AttackSubTechnique.objects.exclude(attackid=".000")
    ttp_count = attackTactics.count() + attackTechniques.count() + attackSubTechniques.count()

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    context = {'attackTechniques': attackTechniques, 'apt_count': apt_count, 'objective_count': objective_count, 'ttp_count': ttp_count}
    return render(request, 'base/attackTechnique.html', context)

@login_required(login_url='login')
def newAttackTechnique(request):
    form = AttackTechniqueForm()

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    if request.method == 'POST':
        form = AttackTechniqueForm(request.POST)

        if form.is_valid():
            attackTechnique = form.save(commit=False) 
            attackTechnique.save()
            messages.success(request, 'Technique created successfully!')
            return redirect('attackTechnique')

    context = {'form': form}
    return render(request, 'base/newAttackTechnique.html', context)

@login_required(login_url='login')
def updateAttackTechnique(request, pk):
    attackTechnique = AttackTechnique.objects.get(id=pk)
    form = AttackTechniqueForm(instance=attackTechnique)

    if request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        form = AttackTechniqueForm(request.POST, instance=attackTechnique)

        if form.is_valid():
            form.save()
            messages.success(request, 'Technique updated successfully!')
            return redirect('attackTechnique')
    
    context = {'form': form}
    return render(request, 'base/updateAttackTechnique.html', context)

@login_required(login_url='login')
def deleteAttackTechnique(request, pk):
    attackTechnique = AttackTechnique.objects.get(id=pk)

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    if request.method == 'POST':
        attackTechnique.delete()
        messages.success(request, 'Technique deleted successfully!')

        return redirect('attackTechnique')

    return render(request, 'base/delete.html', {'obj': attackTechnique})

@login_required(login_url='login')
def attackSubTechnique(request):
    apts = APT.objects.all()
    apt_count = apts.count()

    objectives = Objective.objects.all()
    objective_count = objectives.count()

    attackTactics = AttackTactic.objects.all()
    attackTechniques = AttackTechnique.objects.all()
    attackSubTechniques = AttackSubTechnique.objects.all()
    exclusions = AttackSubTechnique.objects.exclude(attackid=".000")
    ttp_count = attackTactics.count() + attackTechniques.count() + exclusions.count()

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    context = {'attackSubTechniques': attackSubTechniques, 'apt_count': apt_count, 'objective_count': objective_count, 'ttp_count': ttp_count, 'exclusions': exclusions}
    return render(request, 'base/attackSubTechnique.html', context)

@login_required(login_url='login')
def newAttackSubTechnique(request):
    form = AttackSubTechniqueForm()

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    if request.method == 'POST':
        form = AttackSubTechniqueForm(request.POST)

        if form.is_valid():
            attackSubTechnique = form.save(commit=False) 
            attackSubTechnique.save()
            messages.success(request, 'Sub-Technique created successfully!')
            return redirect('attackSubTechnique')

    context = {'form': form}
    return render(request, 'base/newAttackSubTechnique.html', context)

@login_required(login_url='login')
def updateAttackSubTechnique(request, pk):
    attackSubTechnique = AttackSubTechnique.objects.get(id=pk)
    form = AttackSubTechniqueForm(instance=attackSubTechnique)

    if request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        form = AttackSubTechniqueForm(request.POST, instance=attackSubTechnique)

        if form.is_valid():
            form.save()
            messages.success(request, 'Sub-Technique updated successfully!')
            return redirect('attackSubTechnique')
    
    context = {'form': form}
    return render(request, 'base/updateAttackSubTechnique.html', context)

@login_required(login_url='login')
def deleteAttackSubTechnique(request, pk):
    attackSubTechnique = AttackSubTechnique.objects.get(id=pk)

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    if request.method == 'POST':
        attackSubTechnique.delete()
        messages.success(request, 'Sub-Technique deleted successfully!')

        return redirect('attackSubTechnique')

    return render(request, 'base/delete.html', {'obj': attackSubTechnique})

@login_required(login_url='login')
def newGlob(request, pk):
    technique = Technique.objects.get(id=pk)
    form = GlobForm()

    if request.method == 'POST':
        form = GlobForm(request.POST)

        if form.is_valid():
            glob = form.save(commit=False) 
            glob.Technique = technique
            glob.save()
            messages.success(request, 'Globfuscation created successfully!')
            return redirect('variant', pk=glob.Technique.id)

    context = {'form': form}
    return render(request, 'base/newGlob.html', context)

@login_required(login_url='login')
def updateGlob(request, pk):
    glob = Glob.objects.get(id=pk)
    form = GlobForm(instance=glob)

    if request.user.is_superuser != 1:
        return redirect('forbidden')  

    if request.method == 'POST':
        form = GlobForm(request.POST, instance=glob)

        if form.is_valid():
            form.save()
            messages.success(request, 'Globfuscation updated successfully!')
            return redirect('variant', pk=glob.Technique.id)
    
    context = {'form': form}
    return render(request, 'base/updateGlob.html', context)

@login_required(login_url='login')
def deleteGlob(request, pk):
    glob = Glob.objects.get(id=pk)

    if request.user.is_superuser != 1:
        return redirect('forbidden') 

    if request.method == 'POST':
        glob.delete()
        messages.success(request, 'Globfuscation deleted successfully!')

        return redirect('variant', pk=glob.Technique.id)

    return render(request, 'base/delete.html', {'obj': glob})

@login_required(login_url='login')
def report(request):
    userScans = Scan.objects.filter(user=request.user).order_by('created')

    action_list = []
    blocked_list = []
    compromised_list = []
    untested_list = []
    score_list = []

    for scan in userScans:
        threat_count = 0
        blocked_count = 0
        compromised_count = 0
        untested_count = 0
        score_count = 0

        for simulation in scan.simulation_set.all():
            for userVariant in simulation.UserVariant.all():
                threat_count += 1

                if userVariant.detected == False:
                    compromised_count += 1
                elif userVariant.detected == True:
                    blocked_count += 1
                else:
                    untested_count += 1

        if threat_count - untested_count == 0:
            score_count = 0
        else:
            score_count = (compromised_count / (threat_count - untested_count)) * 100
            score_count = round(score_count)

        action_list.append(threat_count)
        blocked_list.append(blocked_count)
        compromised_list.append(compromised_count)
        untested_list.append(untested_count)
        score_list.append(score_count)

    score = (addIndex(compromised_list) / (addIndex(action_list) - addIndex(untested_list))) * 100
    score = round(score)

    context = {'threat_count': addIndex(action_list), 'blocked_count': addIndex(blocked_list), 'compromised_count': addIndex(compromised_list), 'untested_count': addIndex(untested_list), 'score': score, 'score_list': score_list, 'userScans': userScans, 'action_list': action_list}

    return render(request, 'base/report.html', context)

@login_required(login_url='login')
def exportExcel(request, pk):
    scan = Scan.objects.get(id=pk)

    file_name = scan.name.replace(" ", "_")
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{file_name}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(scan.name)

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Simulation', 'Variant', 'Severity', 'Objective', 'Binary', 'ATT&CK ID', 'Tactic', 'Technique', 'Sub-technique', 'Detection Status', 'Payload']

    # Populate Headers
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Reset font for body
    font_style = xlwt.XFStyle()

    variants = UserVariant.objects.filter(simulation__Scan__id=scan.pk).annotate(
        binary=Concat('Variant__Technique__name', Value('.exe')),
        attackID=Concat('Variant__AttackSubTechnique__AttackTechnique__AttackTactic__attackid', Value(':'), 'Variant__AttackSubTechnique__AttackTechnique__attackid', 'Variant__AttackSubTechnique__attackid'),
    )
    rows = variants.values_list('simulation__name', 'name', 'Variant__severity', 'Variant__Objective__name', 'binary', 'attackID', 'Variant__AttackSubTechnique__AttackTechnique__AttackTactic__name', 'Variant__AttackSubTechnique__AttackTechnique__name', 'Variant__AttackSubTechnique__name', 'detected', 'payload')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

@login_required(login_url='login')
def exportJson(request, pk):
    scan = Scan.objects.get(id=pk)

    scanList = []
    simulationList = []

    for simulation in scan.simulation_set.all():
        variantList = []

        for userVariant in simulation.UserVariant.all():
            tempID = userVariant.Variant.AttackSubTechnique.AttackTechnique.AttackTactic.attackid + ":" + userVariant.Variant.AttackSubTechnique.AttackTechnique.attackid

            if userVariant.Variant.AttackSubTechnique.attackid != ".000":
                    tempID += userVariant.Variant.AttackSubTechnique.attackid

            globals()[f"variantDict_{userVariant.id}"] = {"name": userVariant.name, "binary": userVariant.Variant.Technique.name + ".exe", "severity": userVariant.Variant.severity, "objective": userVariant.Variant.Objective.name, "attackID": tempID, "payload": userVariant.payload}

            variantList.append(globals()[f"variantDict_{userVariant.id}"])

        globals()[f"simulationDict_{simulation.id}"] = {"name": simulation.name, "variants": variantList}
        simulationList.append(globals()[f"simulationDict_{simulation.id}"])

    globals()[f"scanDict_{scan.id}"] = {"name": scan.name, "description": scan.description, "updated": scan.updated, "created": scan.created, "simulations": simulationList}
    scanList.append(globals()[f"scanDict_{scan.id}"])

    return HttpResponse(json.dumps(scanList, indent=4, default=str), content_type="application/json")

def forbidden(request):
    return render(request, 'base/forbidden.html')

def notFound(request, exception):
    return render(request, 'base/404.html')