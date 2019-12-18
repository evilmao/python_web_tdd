from django.shortcuts import render, redirect

from .models import Item


# Create your views here.

def home_page(request):
    """home_page 视图函数"""
    if request.method == 'POST':  # 判断请求方式为'post'时
        new_item_text = request.POST['item_text']  # 获取前端提交的值赋值给变量
        Item.objects.create(text=new_item_text)  # 使用ORM, create方法保存数据
        return redirect('/lists/home_page/')
    # else:
    #     new_item_text = ''
    # context = {'new_item_text': new_item_text}
    # 当使用其他请求方式时,直接返回渲染模板
    items = Item.objects.all()
    return render(request, 'home.html',{'items':items})
