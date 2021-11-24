from .models import Category

def categories(request):
    parent_cats = Category.objects.filter(parent=None)
    
    return {'categories': parent_cats}
