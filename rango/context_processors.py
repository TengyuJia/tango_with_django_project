from .models import Category  # 假设你的分类模型叫 Category

def categories(request):
    return {
        'categories': Category.objects.all()  # 获取所有分类
    }