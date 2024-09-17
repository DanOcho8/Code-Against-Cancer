from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

CANCER_TYPE_CHOICES = [
    ('', 'Select your cancer type:'),
    ('bone', 'Bone Cancer'),
    ('brain_nervous', 'Brain and Nervous System Cancer'),
    ('breast', 'Breast Cancer'),
    ('colorectal', 'Colorectal Cancer'),
    ('digestive', 'Digestive System Cancer'),
    ('endocrine', 'Endocrine System Cancer'),
    ('eye', 'Eye Cancer'),
    ('genitourinary', 'Genitourinary Cancer'),
    ('gynecologic', 'Gynecologic Cancer'),
    ('head_neck', 'Head and Neck Cancer'),
    ('hematologic', 'Hematologic Cancer'),
    ('liver', 'Liver Cancer'),
    ('lung', 'Lung Cancer'),
    ('lymphoma', 'Lymphoma'),
    ('melanoma_skin', 'Melanoma and Skin Cancer'),
    ('oral', 'Oral Cancer'),
    ('pancreatic', 'Pancreatic Cancer'),
    ('prostate', 'Prostate Cancer'),
    ('sarcoma', 'Sarcoma'),
    ('stomach', 'Stomach Cancer'),
]

CANCER_STAGE_CHOICES = [
    ('', 'Select cancer stage:'),
    ('I', 'Stage I'),
    ('II', 'Stage II'),
    ('III', 'Stage III'),
    ('IV', 'Stage IV'),
]

GENDER_CHOICES = [
    ('', 'Select your gender:'),
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    cancer_type = forms.ChoiceField(choices=CANCER_TYPE_CHOICES, label="Cancer Type")
    date_diagnosed = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date Diagnosed")  # Single date field
    cancer_stage = forms.ChoiceField(choices=CANCER_STAGE_CHOICES)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    profile_pic = forms.ImageField(required=False, label="Profile Pic (Optional)")  # Label with "Optional"

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'cancer_type', 'date_diagnosed', 'cancer_stage', 'gender', 'profile_pic']

    

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Check if UserProfile exists before creating
            user_profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'cancer_type': self.cleaned_data['cancer_type'],
                    'date_diagnosed': self.cleaned_data['date_diagnosed'],
                    'cancer_stage': self.cleaned_data['cancer_stage'],
                    'gender': self.cleaned_data['gender'],
                    'profile_pic': self.cleaned_data.get('profile_pic')
                }
            )
            if not created:  # Update the existing profile with new data
                user_profile.cancer_type = self.cleaned_data['cancer_type']
                user_profile.date_diagnosed = self.cleaned_data['date_diagnosed']
                user_profile.cancer_stage = self.cleaned_data['cancer_stage']
                user_profile.gender = self.cleaned_data['gender']
                user_profile.profile_pic = self.cleaned_data.get('profile_pic')
                user_profile.save()

            subject = "Your Account Has Been Created!"
            context = {'user': user}
            email_html_message = render_to_string('registration/signup_confirmation_email.html', context)
            email_plaintext_message = strip_tags(email_html_message)

            send_mail(
                subject,
                email_plaintext_message,
                'codeagainstcancer@gmail.com',
                [user.email],
                html_message=email_html_message
            ) 

        return user
    
class UpdateUserForm(UserChangeForm):
    # Hide Password 
    password = None
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    cancer_type = forms.ChoiceField(choices=CANCER_TYPE_CHOICES)
    date_diagnosed = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)))
    cancer_stage = forms.ChoiceField(choices=CANCER_STAGE_CHOICES)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'cancer_type', 'date_diagnosed', 'cancer_stage', 'gender', 'profile_pic']

    

    def save(self, commit=True):
        user = super(UpdateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Check if UserProfile exists before creating
            user_profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'cancer_type': self.cleaned_data['cancer_type'],
                    'date_diagnosed': self.cleaned_data['date_diagnosed'],
                    'cancer_stage': self.cleaned_data['cancer_stage'],
                    'gender': self.cleaned_data['gender'],
                    'profile_pic': self.cleaned_data.get('profile_pic')
                }
            )
            if not created:  # Update the existing profile with new data
                user_profile.cancer_type = self.cleaned_data['cancer_type']
                user_profile.date_diagnosed = self.cleaned_data['date_diagnosed']
                user_profile.cancer_stage = self.cleaned_data['cancer_stage']
                user_profile.gender = self.cleaned_data['gender']
                user_profile.profile_pic = self.cleaned_data.get('profile_pic')
                user_profile.save()

        return user