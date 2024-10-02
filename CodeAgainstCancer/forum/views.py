from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Thread, Post
from .forms import PostForm, ReplyForm, CreateThreadForm
# Function to list all threads
def thread_list(request):
    threads = Thread.objects.all()  # Get all threads
    return render(request, 'forum/thread_list.html', {'object_list': threads})

# Function to view a specific thread and its posts
@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    posts = thread.posts.all()

    # Handle new posts
    if request.method == 'POST' and 'post_form' in request.POST:
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.thread = thread
            post.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        post_form = PostForm()

    # Handle replies
    if request.method == 'POST' and 'reply_form' in request.POST:
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.author = request.user
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            reply.post = post
            reply.save()

            # Return JSON response
            return JsonResponse({
                'success': True,
                'reply': reply.content,
                'author': reply.author.username,
                'created_at': reply.created_at.strftime("%B %d, %Y, %I:%M %p")
            })

    reply_form = ReplyForm()
    
    return render(request, 'forum/thread_detail.html', {
        'object': thread,
        'posts': posts,
        'post_form': post_form,
        'reply_form': reply_form,
    })




# Function to create a new thread
def create_thread(request):
    if request.method == 'POST':
        form = CreateThreadForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new thread
            return redirect('thread_list')  # Redirect to the thread list
    else:
        form = CreateThreadForm()

    return render(request, 'forum/create_thread.html', {'form': form})

# Function to create a new post within a thread
def create_post(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.thread = thread  # Associate post with the thread
            post.save()  # Save the post
            return redirect('thread_detail', pk=thread.pk)  # Redirect to thread detail
    else:
        form = PostForm()
    
    return render(request, 'forum/create_post.html', {'form': form, 'thread': thread})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReplyForm
from .models import Post

@login_required
def reply_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # Get the post being replied to

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user  # Set the author to the current user
            reply.thread = post.thread  # Associate the reply with the original thread
            reply.save()  # Save the reply
            
            # Return JSON response with reply data
            return JsonResponse({
                'success': True,
                'reply': reply.content,  # Assuming reply has a 'content' field
                'author': reply.author.username,
                'created_at': reply.created_at.strftime("%Y-%m-%d %H:%M:%S")  # Format as needed
            })

    return JsonResponse({'success': False, 'error': 'Invalid form submission.'})  # Handle invalid case



