from django import forms
from .models import Thread, Post

class CreateThreadForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control',
            'style': 'width: 100%; min-height: 100px; padding: 12px; font-size: 14px; border-radius: 10px; border: 1px solid #ddd; resize: none; overflow: hidden;',
            'placeholder': 'Write the first post of the thread here...'
        }), label="Your Post")

    class Meta:
        model = Thread
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Your Topic/Question',  
        }

    def save(self, user, commit=True):  
        thread = super().save(commit=False)
        thread.author = user 
        if commit:
            thread.save()
            # Create the first post as part of the thread and assign the author
            Post.objects.create(
                thread=thread,
                content=self.cleaned_data['content'],
                author=user,  # Assign the logged-in user as the author
            )
        return thread

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control',
            'style': 'width: 100%; min-height: 100px; padding: 12px; font-size: 14px; border-radius: 10px; border: 1px solid #ddd; resize: none; overflow: hidden;',
            'placeholder': 'Write your post here...'
        }), label="Post Content")

    class Meta:
        model = Post
        fields = ['content']


class ReplyForm(forms.ModelForm):
    content = forms.CharField(
        label="Add your reply",  
        widget=forms.Textarea(attrs={
            'style': 'width: 100%; min-height: 50px; resize: none; overflow: hidden; padding: 8px; font-size: 14px; border-radius: 10px; border: 1px solid #ddd;',
            'rows': '1',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Post
        fields = ['content']
