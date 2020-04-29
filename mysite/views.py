from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.contenttypes.fields import ContentType
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from read_statistic.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data, \
    get_seven_days_hot_blogs
from blog.models import Blog
from .forms import LoginForm, RegForm


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    seven_days_hot_blogs = cache.get('seven_days_hot_blogs')
    if seven_days_hot_blogs is None:
        seven_days_hot_blogs = get_seven_days_hot_blogs(content_type=blog_content_type)
        cache.set('seven_days_hot_blogs', seven_days_hot_blogs, 3600)

    # 获取今天热门博客的缓存数据
    today_hot_data = get_today_hot_data(content_type=blog_content_type)

    yesterday_hot_data = get_yesterday_hot_data(content_type=blog_content_type)
    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['seven_days_hot_blogs'] = seven_days_hot_blogs
    return render(request, 'home.html', context)


def login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def register(request):
    if request.method == "POST":
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()

            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)
