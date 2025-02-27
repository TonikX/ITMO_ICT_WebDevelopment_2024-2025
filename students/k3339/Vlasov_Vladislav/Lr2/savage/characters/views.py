from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from .models import Character, CharactersAttribute, CharactersSkill, Attribute, Skill
from .forms import CharactersCreateForm, CharactersUpdateForm
# Create your views here.

def createNewUser(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form })

def getAllCharacters(request):

    if request.user.is_authenticated:
        context = {}
        context["own_char"] = Character.objects.filter(owner=request.user)
        context["other_char"] = Character.objects.exclude(owner=request.user)
        return render(request, 'campaign/all_characters.html', context)
    
    else:
        return render(request, 'registration/not_authenticated.html')
    
def my_logout(request):
    logout(request)
    return render(request, 'registration/logout.html')

def createCharactersAttributes(request):

    if not request.user.is_authenticated:
        return render(request, 'registration/not_authenticated.html')

    attributes = Attribute.objects.all()
    skills = Skill.objects.all()
    
    if request.method == 'POST':
        form = CharactersCreateForm(request.POST, attributes=attributes, skills=skills)
        if form.is_valid():
            char = Character.objects.create(
                name = request.POST.get(f'name'),
                owner = request.user,
                bennies = 3,
                wounds = 0,
                fatigue = 0,
                appearance = request.POST.get(f'appearance'),
                slogan = request.POST.get(f'slogan'),
            )
            char.save()
            
            for attribute in attributes:
                value = request.POST.get(f'attribute_value_{attribute.id}_{attribute.name}')
                bonus = request.POST.get(f'attribute_bonus_{attribute.id}_{attribute.name}')
                charAttribute = CharactersAttribute.objects.create(
                    character = char,
                    attribute=attribute,
                    value=value or 0,
                    bonus=bonus or 0
                )
                charAttribute.save()

            for skill in skills:
                value = request.POST.get(f'skill_value_{skill.id}_{skill.name}')
                bonus = request.POST.get(f'skill_bonus_{skill.id}_{skill.name}')
                charSkill = CharactersSkill.objects.create(
                    character = char,
                    skill=skill,
                    value=value or 0,
                    bonus=bonus or 0 if value != "0" else -2
                )
                charSkill.save()

            return redirect('/characters/list/')

    form = CharactersCreateForm(attributes=attributes, skills=skills)
    return render(request, 'campaign/create_character.html', {'form': form})

def updateCharactersAttributes(request, pk):

    if not request.user.is_authenticated:
        return render(request, 'registration/not_authenticated.html')

    attributes = Attribute.objects.all()
    skills = Skill.objects.all()

    char = Character.objects.get(id=pk)

    if char.owner.id != request.user.id and not request.user.groups.filter(name="Мастера"):
        return render(request, 'registration/not_access.html')

    charAttributes = CharactersAttribute.objects.filter(character=char.id)
    charSkills = CharactersSkill.objects.filter(character=char.id)

    initial_value = {
        'bennies': char.bennies,
        'wounds': char.wounds,
        'fatigue': char.fatigue,
        'name': char.name,
        'appearance': char.appearance,
        'slogan': char.slogan,
    }        
    for charAttribute in charAttributes:
        initial_value[f'attribute_value_{charAttribute.attribute.id}'] = charAttribute.value
        initial_value[f'attribute_bonus_{charAttribute.attribute.id}'] = charAttribute.bonus
    for charSkill in charSkills:
        initial_value[f'skill_value_{charSkill.skill.id}'] = charSkill.value
        initial_value[f'skill_bonus_{charSkill.skill.id}'] = charSkill.bonus

    if request.method == 'POST':
        form = CharactersUpdateForm(request.POST, attributes=attributes, skills=skills, initial_value=initial_value)
        if form.is_valid():
            print('hi')
            char.name = request.POST.get(f'name') if request.POST.get(f'name') != None else char.name
            char.bennies = request.POST.get(f'bennies') if request.POST.get(f'bennies') != None else char.bennies
            char.wounds = request.POST.get(f'wounds') if request.POST.get(f'wounds') != None else char.wounds
            char.fatigue = request.POST.get(f'fatigue') if request.POST.get(f'fatigue') != None else char.fatigue
            char.appearance = request.POST.get(f'appearance') if request.POST.get(f'appearance') != None else char.appearance
            char.slogan = request.POST.get(f'slogan') if  request.POST.get(f'slogan') != None else char.slogan
            char.save()
            
            for attribute in charAttributes:
                attribute.value = request.POST.get(f'attribute_value_{attribute.attribute.id}_{attribute.attribute}') if request.POST.get(f'attribute_value_{attribute.attribute.id}_{attribute.attribute}') != None else attribute.value
                attribute.bonus = request.POST.get(f'attribute_bonus_{attribute.attribute.id}_{attribute.attribute}') if request.POST.get(f'attribute_bonus_{attribute.attribute.id}_{attribute.attribute}')  != None else attribute.bonus
                attribute.save()

            for skill in charSkills:
                skill.value = request.POST.get(f'skill_value_{skill.skill.id}_{skill.skill}') if request.POST.get(f'skill_value_{skill.skill.id}_{skill.skill}') != None else skill.value
                skill.bonus = request.POST.get(f'skill_bonus_{skill.skill.id}_{skill.skill}') if request.POST.get(f'skill_bonus_{skill.skill.id}_{skill.skill}') != None else skill.bonus
                skill.save()

            charAttributesIds = charAttributes.values_list('attribute__id', flat=True)
            for attribute in attributes:
                if not attribute.id in charAttributesIds:
                    value = request.POST.get(f'attribute_value_{attribute.id}_{attribute.name}')
                    bonus = request.POST.get(f'attribute_bonus_{attribute.id}_{attribute.name}')
                    charAttribute = CharactersAttribute.objects.create(
                        character = char,
                        attribute=attribute,
                        value=value or 0,
                        bonus=bonus or 0
                    )
                    charAttribute.save()

            charSkillsIds = charSkills.values_list('skill__id', flat=True)
            for skill in skills:
                if not skill.id in charSkillsIds:
                    value = request.POST.get(f'skill_value_{skill.id}_{skill.name}')
                    bonus = request.POST.get(f'skill_bonus_{skill.id}_{skill.name}')
                    charSkill = CharactersSkill.objects.create(
                        character = char,
                        skill=skill,
                        value=value or 0,
                        bonus=bonus or 0
                    )
                    charSkill.save()

            return redirect(f'/character/{pk}')

    form = CharactersUpdateForm(attributes=attributes, skills=skills, initial_value=initial_value)
    return render(request, 'campaign/update_character.html', {'form': form})

def getCharacter(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'registration/not_authenticated.html')
    
    char = Character.objects.get(id=pk)

    if char.owner.id != request.user.id and not request.user.groups.filter(name="Мастера"):
        return render(request, 'registration/not_access.html')
    
    context = {}

    context['char'] = char

    charAttributes = CharactersAttribute.objects.filter(character=pk)
    charSkills = CharactersSkill.objects.filter(character=pk)
    
    context['attributes'] = charAttributes
    context['skills_by_attribute'] = {}

    for attribute in char.attributes.all():
        context['skills_by_attribute'][attribute] = charSkills.filter(skill__attribute=attribute)


    template_name = "campaign/character.html"
    return render(request, template_name, context)

class deleteCharacter(UserPassesTestMixin, DeleteView):
    model = Character
    template_name = "campaign/delete_character.html"
    success_url = '/characters/list/'

    def test_func(self):
        char = self.get_object()
        return self.request.user.groups.filter(name="Мастера").exists() or char.owner.id == self.request.user.id

    def handle_no_permission(self):
        return render(self.request, template_name='registration/not_access.html')

class getSkills(UserPassesTestMixin, ListView):
    model = Skill
    template_name = "campaign/skills.html"

    def test_func(self):
        return self.request.user.groups.filter(name="Мастера").exists()

    def handle_no_permission(self):
        return render(self.request, template_name='registration/not_access.html')
    
class updateSkill(UserPassesTestMixin, UpdateView):
    model = Skill
    template_name = "campaign/update_skill.html"
    fields = ['name', 'attribute']
    success_url = '/skills/list/'

    def test_func(self):
        return self.request.user.groups.filter(name="Мастера").exists()

    def handle_no_permission(self):
        return render(self.request, template_name='registration/not_access.html')
    
class deleteSkill(UserPassesTestMixin, DeleteView):
    model = Skill
    template_name = "campaign/delete_skill.html"
    success_url = '/skills/list/'

    def test_func(self):
        return self.request.user.groups.filter(name="Мастера").exists()

    def handle_no_permission(self):
        return render(self.request, template_name='registration/not_access.html')
    
class createSkill(UserPassesTestMixin, CreateView):
    model = Skill
    template_name = "campaign/create_skill.html"
    fields = ['name', 'attribute']
    success_url = '/skills/list/'

    def test_func(self):
        return self.request.user.groups.filter(name="Мастера").exists()

    def handle_no_permission(self):
        return render(self.request, template_name='registration/not_access.html')