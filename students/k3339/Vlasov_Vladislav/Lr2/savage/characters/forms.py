from django import forms
from .models import Attribute, Skill, Character, CharactersAttribute


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name']


class CharactersCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        attributes = kwargs.pop('attributes')
        super().__init__(*args, **kwargs)
        for attribute in attributes:
            self.fields[f'value_{attribute.id}'] = forms.IntegerField(
                label=attribute.name,
                min_value=1,
                max_value=5,
                initial=1,
            )
            self.fields[f'bonus_{attribute.id}'] = forms.IntegerField(
                label=f'{attribute.name} Bonus',
                required=False,
                initial=0,
            )


class CharactersCreateForm(forms.Form):

    def __init__(self, *args, **kwargs):

        attributes = kwargs.pop('attributes')
        skills = kwargs.pop('skills')

        initial_value = {}
        if 'initial_value' in kwargs:
            initial_value = kwargs.pop('initial_value')
        
        super().__init__(*args, **kwargs)

        self.create_form(attributes, skills, initial_value)

    def create_form(self, attributes, skills, initial_value):

        self.fields['name'] = forms.CharField(
            label='Введите имя ',
            initial = initial_value['name'] if 'name' in initial_value else ''
        )

        self.fields['appearance'] = forms.CharField(
            label='Внешность ',
            required = False,
            initial = initial_value['appearance'] if 'appearance' in initial_value else '',
            widget=forms.Textarea(attrs={'rows': 4, 'cols': 40})
        )

        self.fields['slogan'] = forms.CharField(
            label='Ваш девиз! ',
            required = False,
            initial = initial_value['slogan'] if 'slogan' in initial_value else '',
            widget=forms.Textarea(attrs={'rows': 4, 'cols': 40})
        )
        
        for attribute in attributes:

            self.fields[f'attribute_value_{attribute.id}_{attribute.name}'] = forms.ChoiceField(
                label = "Кость ",
                choices = [
                    (1, 'd4'),
                    (2, 'd6'),
                    (3, 'd8'),
                    (4, 'd10'),
                    (5, 'd12'),
                ],
                initial = initial_value[f'attribute_value_{attribute.id}'] if f'attribute_value_{attribute.id}' in initial_value else 1,
                widget = forms.Select(attrs={'name': f'value_{attribute.id}'}),
            )

            self.fields[f'attribute_bonus_{attribute.id}_{attribute.name}'] = forms.IntegerField(
                label="Бонус ",
                required=False,
                initial=initial_value[f'attribute_bonus_{attribute.id}'] if f'attribute_bonus_{attribute.id}' in initial_value else 0,
            )

            for skill in skills.filter(attribute=attribute):
                
                self.fields[f'skill_value_{skill.id}_{skill.name}'] = forms.ChoiceField(
                    label ="Кость ",
                    choices=[
                        (0, 'нет'),
                        (1, 'd4'),
                        (2, 'd6'),
                        (3, 'd8'),
                        (4, 'd10'),
                        (5, 'd12'),
                    ],
                    initial=initial_value[f'skill_value_{skill.id}'] if f'skill_value_{skill.id}' in initial_value else 0,
                    widget=forms.Select(attrs={'name': f'value_{skill.id}'})
                )

                self.fields[f'skill_bonus_{skill.id}_{skill.name}'] = forms.IntegerField(
                    label="Бонус ",
                    required=False,
                    initial=initial_value[f'skill_bonus_{skill.id}'] if f'skill_bonus_{skill.id}' in initial_value else 0,
                )


class CharactersUpdateForm(CharactersCreateForm):

    def create_form(self, attributes, skills, initial_value):

        self.fields['bennies'] = forms.IntegerField(
            label='Фишки ',
            initial = initial_value['bennies'] if 'bennies' in initial_value else 0,
        )

        self.fields['wounds'] = forms.IntegerField(
            label='Раны ',
            initial = initial_value['wounds'] if 'wounds' in initial_value else 0,
            min_value=0,
            max_value=3,
        )

        self.fields['fatigue'] = forms.IntegerField(
            label='Усталость ',
            initial = initial_value['fatigue'] if 'fatigue' in initial_value else 0,
            min_value=0,
            max_value=2,
        )

        super().create_form(attributes, skills, initial_value)