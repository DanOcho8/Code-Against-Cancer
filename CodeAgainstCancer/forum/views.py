from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from .models import Thread, Post
from .forms import PostForm, ReplyForm, CreateThreadForm
from django.utils import timezone
# Function to list all threads
def thread_list(request):
    threads = Thread.objects.all()  # Get all threads
    return render(request, 'forum/thread_list.html', {'object_list': threads})

# Function to view a specific thread and its posts
@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    posts = thread.posts.filter(parent_post__isnull=True)  # Fetch main posts only
    replies = thread.posts.filter(parent_post__isnull=False)  # Fetch replies only

    # Handle new posts
    if request.method == 'POST' and 'post_form' in request.POST:
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.thread = thread
            post.author = request.user  # Set the current user as the author
            post.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        post_form = PostForm()

    # Handle replies
    if request.method == 'POST' and 'reply_form' in request.POST:
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.author = request.user  # Set the current user as the author
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            reply.post = post  # Associate reply with the post
            reply.save()
            return redirect('thread_detail', pk=thread.pk)

    reply_form = ReplyForm()

    return render(request, 'forum/thread_detail.html', {
        'object': thread,
        'posts': posts,
        'replies': replies,
        'post_form': post_form,
        'reply_form': reply_form,
    })




# Function to create a new thread
@login_required
def create_thread(request):
    if request.method == 'POST':
        form = CreateThreadForm(request.POST)
        if form.is_valid():
            # Save the form and pass the user for the post's author
            thread = form.save(user=request.user)
            return redirect('thread_list')
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


@login_required
def reply_to_post(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        post = get_object_or_404(Post, id=post_id)
        thread = post.thread

        # Create the new reply
        reply = Post.objects.create(
            content=content,
            author=request.user,
            thread=thread,
            parent_post=post
        )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check for AJAX request
            return JsonResponse({
                'success': True,
                'reply': reply.content,
                'author': reply.author.username,
                'created_at': reply.created_at.strftime('%B %d, %Y, %I:%M %p'),
                'parent_post_id': post.id
            })
        
        # If not an AJAX request, redirect as usual
        return redirect('thread_detail', pk=thread.pk)

    return redirect('thread_detail', pk=post.thread.pk)


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user == post.author:
        post.delete()
        return redirect('thread_detail', pk=post.thread.pk)
    else:
        return redirect('thread_detail', pk=post.thread.pk)
    