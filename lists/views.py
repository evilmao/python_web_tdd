from django.shortcuts import render, redirect

from .models import Item


# Create your views here.

def home_page(request):
    """home_page 视图函数"""
    if request.method == 'POST':  # 判断请求方式为'post'时
        new_item_text = request.POST['item_text']  # 获取前端提交的值赋值给变量
        Item.objects.create(text=new_item_text)  # 使用ORM, create方法保存数据
        return redirect('/lists/the-only-list-in-the-world/')
    # else:
    #     new_item_text = ''
    # context = {'new_item_text': new_item_text}
    # 当使用其他请求方式时,直接返回渲染模板
    # 在 home_page 视图中其实也不用把全部待办事项都传入 home.html 模板
    #return render(request, 'home.html',{'items':items})
    # 可以简化成如下
    return render(request, 'home.html')

def view_list(request):
    """list 视图函数"""
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
