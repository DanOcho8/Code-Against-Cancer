from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from phonenumber_field.formfields import PhoneNumberField
from .area_codes import AREA_CODE_CHOICES

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
    area_code = forms.CharField(
        label="Area Code",
        max_length=5,
        widget=forms.TextInput(attrs={'id': 'id_area_code'})
    )
    phone_number = forms.CharField(required=False, label="Phone Number")
    cancer_type = forms.ChoiceField(choices=CANCER_TYPE_CHOICES, label="Cancer Type")
    date_diagnosed = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date Diagnosed"
    )
    cancer_stage = forms.ChoiceField(choices=CANCER_STAGE_CHOICES, label="Cancer Stage")
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Gender")
    profile_pic = forms.ImageField(required=False, label="Profile Pic (Optional)")
    consent_to_text = forms.BooleanField(
        required=False,
        label="I consent to receive text message reminders"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'cancer_type', 'date_diagnosed', 'cancer_stage', 'gender', 'profile_pic', 'consent_to_text']

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        # Combine area code and phone number
        area_code = self.cleaned_data.get('area_code', '')
        phone_number = self.cleaned_data.get('phone_number', '')
        user.phone_number = f"{area_code}{phone_number}"
        
        if commit:
            user.save()
            user_profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'cancer_type': self.cleaned_data['cancer_type'],
                    'date_diagnosed': self.cleaned_data['date_diagnosed'],
                    'cancer_stage': self.cleaned_data['cancer_stage'],
                    'gender': self.cleaned_data['gender'],
                    'profile_pic': self.cleaned_data.get('profile_pic'),
                    'phone_number': user.phone_number,
                    'consent_to_text': self.cleaned_data.get('consent_to_text')
                }
            )
            if not created:
                user_profile.cancer_type = self.cleaned_data['cancer_type']
                user_profile.date_diagnosed = self.cleaned_data['date_diagnosed']
                user_profile.cancer_stage = self.cleaned_data['cancer_stage']
                user_profile.gender = self.cleaned_data['gender']
                user_profile.profile_pic = self.cleaned_data.get('profile_pic')
                user_profile.phone_number = user.phone_number
                user_profile.consent_to_text = self.cleaned_data.get('consent_to_text')
                user_profile.save()

            # Send the confirmation email
            subject = "Your Account Has Been Created!"
            context = {'user': user}
            email_html_message = render_to_string('registration/signup_confirmation_email.html', context)
            email_plaintext_message = strip_tags(email_html_message)
            
            send_mail(
                subject,
                email_plaintext_message,
                'codeagainstcancer@outlook.com',
                [user.email],
                html_message=email_html_message
            )

        return user
    

class UpdateUserForm(UserChangeForm):
    password = None
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    area_code = forms.CharField(
        label="Area Code",
        max_length=5,
        widget=forms.TextInput(attrs={'id': 'id_area_code'})
    )
    phone_number = forms.CharField(required=False, label="Phone Number")
    cancer_type = forms.ChoiceField(choices=CANCER_TYPE_CHOICES)
    date_diagnosed = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date Diagnosed")
    cancer_stage = forms.ChoiceField(choices=CANCER_STAGE_CHOICES)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    profile_pic = forms.ImageField(required=False)
    consent_to_text = forms.BooleanField(required=False, label="I consent to receive text message reminders")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'cancer_type', 'date_diagnosed', 'cancer_stage', 'gender', 'profile_pic', 'consent_to_text']

    def save(self, commit=True):
        user = super(UpdateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        # Combine area code and phone number
        area_code = self.cleaned_data.get('area_code', '')
        phone_number = self.cleaned_data.get('phone_number', '')
        user.phone_number = f"{area_code}{phone_number}"
        
        if commit:
            user.save()
            user_profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'cancer_type': self.cleaned_data['cancer_type'],
                    'date_diagnosed': self.cleaned_data['date_diagnosed'],
                    'cancer_stage': self.cleaned_data['cancer_stage'],
                    'gender': self.cleaned_data['gender'],
                    'profile_pic': self.cleaned_data.get('profile_pic'),
                    'phone_number': user.phone_number, 
                    'consent_to_text': self.cleaned_data.get('consent_to_text')
                }
            )
            if not created:
                user_profile.cancer_type = self.cleaned_data['cancer_type']
                user_profile.date_diagnosed = self.cleaned_data['date_diagnosed']
                user_profile.cancer_stage = self.cleaned_data['cancer_stage']
                user_profile.gender = self.cleaned_data['gender']
                user_profile.profile_pic = self.cleaned_data.get('profile_pic')
                user_profile.phone_number = user.phone_number
                user_profile.consent_to_text = self.cleaned_data.get('consent_to_text')
                user_profile.save()

        return user
