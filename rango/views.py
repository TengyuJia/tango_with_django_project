from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page, UserLike, UserLikePage, RecommendedDish
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm,CommentForm, RecommendedDishForm, PriceForm, RatingForm 
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.serp_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.db import models 
def index(request):
    #return HttpResponse("Rango says hey there partner!<a href=\"http://127.0.0.1:8000/rango/about\">About</a>")
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    all_pages = Page.objects.all() 
    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    context_dict['all_pages'] = all_pages
    visitor_cookie_handler(request)
    context_dict['visits'] =  request.session['visits']
    response = render(request, 'rango/index.html', context=context_dict)
    return response

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug = category_name_slug)
        pages = Page.objects.filter(category = category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    if request.user.is_authenticated:
        context_dict['user_liked'] = UserLike.objects.filter(user=request.user, category=category).exists()
    else:
        context_dict['user_liked'] = False
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            context_dict['result_list'] = run_query(query)
            context_dict['query'] = query
    return render(request, 'rango/category.html', context = context_dict)

def show_page(request, category_name_slug, page_name_slug):
    context_dict = {}
    
    try:
        page = Page.objects.get(slug=page_name_slug)
        context_dict['page'] = page
        comments = page.comments.all()
        context_dict['comments'] = comments
        
        if request.user.is_authenticated:
            context_dict['user_liked_page'] = UserLikePage.objects.filter(user=request.user, page=page).exists()
        else:
            context_dict['user_liked_page'] = False
        recommended_dishes = RecommendedDish.objects.filter(page=page).values('dish_name').annotate(count=models.Count('dish_name')).order_by('-count')[:3]    
        context_dict['recommended_dishes'] = recommended_dishes
        if request.method == 'POST':
            cmt_form = CommentForm(request.POST)
            dish_form = RecommendedDishForm(request.POST)
            price_form = PriceForm(request.POST)
            rating_form = RatingForm(request.POST)
            # update comment form
            if cmt_form.is_valid():
                comment = cmt_form.save(commit=False)
                comment.page = page
                comment.user = request.user  
                comment.save()
                return redirect('rango:show_page', category_name_slug=category_name_slug, page_name_slug=page_name_slug)
            # update dish form    
            if dish_form.is_valid():
                recommended_dishes = dish_form.save(commit=False)
                recommended_dishes.page = page
                recommended_dishes.user = request.user  
                recommended_dishes.save()
                return redirect('rango:show_page', category_name_slug=category_name_slug, page_name_slug=page_name_slug)
            # update price form
            if price_form.is_valid():
                price = price_form.save(commit=False)
                price.page = page
                price.user = request.user
                price.save()
                page.update_average_price()  # calculate average price
                return redirect('rango:show_page', category_name_slug=category_name_slug, page_name_slug=page_name_slug)            
            # update rating form
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.page = page
                rating.user = request.user
                rating.save()
                page.update_average_rating()  # calculate average rating
                return redirect('rango:show_page', category_name_slug=category_name_slug, page_name_slug=page_name_slug)
        else:
            cmt_form = CommentForm()
            dish_form = RecommendedDishForm()
            price_form = PriceForm()
            rating_form = RatingForm()
        
        context_dict['cmt_form'] = cmt_form
        context_dict['dish_form'] = dish_form
        context_dict['price_form'] = price_form
        context_dict['rating_form'] = rating_form
        context_dict['category_name_slug'] = category_name_slug  

    except Page.DoesNotExist:
        # 如果页面不存在，设置标题为 None
        context_dict['title'] = None
        context_dict['page'] = None
        context_dict['comments'] = None
        context_dict['cmt_form'] = None
        context_dict['dish_form'] = None
        context_dict['price_form'] = None
        context_dict['rating_form'] = None
    
    return render(request, 'rango/page.html', context=context_dict)
    
def about(request):
    #return HttpResponse("Rango says this is about the page!<a href = \"http://127.0.0.1:8000/rango\">Index</a>")

    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    return render(request, 'rango/about.html')
    
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=True)
            print(cat, cat.slug)
            return redirect('/rango/')
        else:
            print(form.errors)
    return render(request,'rango/add_category.html',{'form':form})
    
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
# You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug':
                                                category_name_slug}))
            else:
                print(form.errors)
    else:
        form = PageForm()
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
#def search(request):
#    result_list = []
#    if request.method == 'POST':
#        query = request.POST['query'].strip()
#        if query:
#            # Run our Bing function to get the results list!
#            result_list = run_query(query)
#    return render(request, 'rango/search.html', {'result_list': result_list})
    
def goto_url(request):
    page_id = None
    if request.method == 'GET':
        page_id = request.GET.get('page_id')
        if page_id:
            try:            
                selected_page = Page.objects.get(id = int(page_id))
                selected_page.views = selected_page.views + 1
                category_slug = selected_page.category.slug  # 假设 Page 有 category 外键
                page_slug = selected_page.slug  # 假设 Page 有 slug 字段
                selected_page.save()
            except selected_page.DoesNotExist:
                return redirect(reverse('rango:index'))
            return redirect(reverse('rango:show_page', kwargs={
                'category_name_slug': category_slug,
                'page_name_slug': page_slug}))
    return redirect(reverse('rango:index'))
'''    
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
             
            profile =  profile_form.save(commit = False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
                 
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
             
    return render(request,
                    'rango/register.html',
                    context = {'user_form': user_form,
                                'profile_form': profile_form,
                                'registered': registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
''' 

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
   
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
    
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if (datetime.now()- last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits

class LikeCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        category_id = request.GET.get('category_id')
        try:
            category = Category.objects.get(id=int(category_id))
        except (Category.DoesNotExist, ValueError):
            return HttpResponse(-1)  

        if UserLike.objects.filter(user=request.user, category=category).exists():
            return HttpResponse(-2)  

        UserLike.objects.create(user=request.user, category=category)

        category.likes += 1
        category.save()

        return HttpResponse(category.likes)
        
class LikePageView(View):
    @method_decorator(login_required)
    def get(self, request):
        page_id = request.GET.get('page_id')
        try:
            page = Page.objects.get(id=int(page_id))
        except (Page.DoesNotExist, ValueError):
            return HttpResponse(-1)  

        if UserLikePage.objects.filter(user=request.user, page=page).exists():
            return HttpResponse(-2)  

        UserLikePage.objects.create(user=request.user, page=page)

        page.likes += 1
        page.save()

        return HttpResponse(page.likes)