from django.shortcuts import render_to_response
from django.core.cache import cache
from django.contrib.contenttypes.fields import ContentType
from read_statistic.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data, \
    get_seven_days_hot_blogs
from blog.models import Blog


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
    return render_to_response('home.html', context)
