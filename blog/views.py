from django.utils import timezone
from .models import Post, Category
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django import template
from django.http import JsonResponse
from django.template.loader import render_to_string

def post_list(request):
    category = Category.objects.all()
    posts = Post.objects.all().order_by('-published_date')

    ctx = {}
    if request.GET.get("pk"):
        url_parameter = request.GET.get("pk")

        if url_parameter:
            posts = Post.objects.filter(category_id = url_parameter).order_by('-published_date')
        else:
            posts = Post.objects.all().order_by('-published_date')

    if request.GET.get("id"):
        url_parameter = request.GET.get("id")

        if url_parameter:
            posts = Post.objects.filter(title__icontains = url_parameter).order_by('-published_date')
        else:
            posts = Post.objects.all().order_by('-published_date')

    ctx={"posts": posts,"category": category}
    if request.is_ajax():
        html = render_to_string(
            template_name="blog/category_list.html",
            context={"posts": posts,"category": category}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, 'blog/post_list.html', context=ctx)


# def post_list2(request):
#     posts = Post.objects.all().order_by('created_date')

#     title = {}
#     # pythonはviewsでcategoryのpkを取ってきているので、urlにpkの記載は必要ない
#     url_parameter = request.GET.get("id")

#     if url_parameter:
#         posts = Post.objects.filter(title__icontains = url_parameter).order_by('created_date')
#     else:
#         posts = Post.objects.all().order_by('created_date')





def post_detail(request, pk):
    current_user = request.user.id
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post,'current_user':current_user})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, "投稿が完了しました！")
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        if request.method == "POST":
            form = PostForm(request.POST,request.FILES, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                messages.success(request, "編集が完了しました！")
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    posts = user.post_set.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/users_detail.html', {'user': user,'posts': posts})


@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
        return redirect('post_list')