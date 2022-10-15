from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from blog.forms import CommentForm
from django.utils import timezone

# from django.views.decorators.cache import cache_page

import logging
logger = logging.getLogger(__name__)

# from django.views.decorators.vary import vary_on_cookie


# Create your views here.
# @cache_page(300)
# def index(request):
#     posts = Post.objects.all()
#     logger.debug(f'Got {len(posts)} posts')
#     return render(request, "blog/index.html", {"posts":posts})

# @cache_page(300)
# @vary_on_cookie
def index(request):
    # from django.http import HttpResponse
    # return HttpResponse(str(request.user).encode("ascii"))
    # posts = Post.objects.filter(published_at__lte=timezone.now())

    posts = (
    Post.objects.filter(published_at__lte=timezone.now())
    .select_related("author")
    # .defer("created_at", "modified_at")
    )

    logger.debug("Got %d posts", len(posts))
    return render(request, "blog/index.html", {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                logger.info('created comment on Post %d for user %s', post.pk, request.user)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(request, 'blog/post-detail.html', {"post":post, "comment_form":comment_form })

def get_ip(request):
  from django.http import HttpResponse
  return HttpResponse(request.META['REMOTE_ADDR'])