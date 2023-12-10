from django.shortcuts import render
from .models import News, get_object_or_404


def news_list(request):
    news_list = News.objects.order_by('-date_published')
    return render(request, 'news_list.html', {'news_list': news_list})


def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'news': news})
