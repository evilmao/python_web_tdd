from django.shortcuts import render, redirect

from .models import Item, List


# Create your views here.

def home_page(request):
    """home_page 视图函数"""
    return render(request, 'home.html')


def view_list(request,list_id):
    """list 视图函数"""
    list_ = List.objects.get(id=list_id)
    # items = Item.objects.filter(list=list_)  # 可以使用反向查询取第
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    """添加新代办事项视图"""
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'],list=list_)
    return redirect('/lists/{}/'.format(list_.id))


def add_item(request,list_id):
    """添加代办事项到代办列表中"""
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/{}/'.format(list_.id))