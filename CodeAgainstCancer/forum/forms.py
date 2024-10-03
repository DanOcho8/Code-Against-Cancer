from django import forms
from .models import Thread, Post

class CreateThreadForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label="Your Post")

    class Meta:
        model = Thread
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, user, commit=True):  # Add 'user' parameter here
        thread = super().save(commit=False)
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
    content = forms.CharField(widget=forms.Textarea, label="Post Content")

    class Meta:
        model = Post
        fields = ['content']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
