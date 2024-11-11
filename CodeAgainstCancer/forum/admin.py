from django.contrib import admin
from .models import Thread, Post, Reply

admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Reply)