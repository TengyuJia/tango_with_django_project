from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page, UserLike, UserLikePage, RecommendedDish, ContactUs
from rango.forms import CategoryForm, PageForm, UserProfileForm, CommentForm, RecommendedDishForm, PriceForm, RatingForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.serp_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.db import models 

# Homepage view
def index(request):
    query = request.GET.get('query', '')  # Get search query
    category_list = Category.objects.order_by('-likes')[:5]  # Top 5 categories by likes
    page_list = Page.objects.order_by('-views')[:5]  # Top 5 pages by views
    if query:
        all_pages = Page.objects.filter(Q(title__icontains=query) | Q(category__name__icontains=query))  # Search pages
    else:
        all_pages = Page.objects.all()
    context_dict = {}
    context_dict['categories_'] = category_list
    context_dict['pages'] = page_list
    context_dict['all_pages'] = all_pages
    visitor_cookie_handler(request)  # Handle visitor cookies
    context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/index.html', context=context_dict)
    return response

# Show category view
def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)  # Get category by slug
        pages = Page.objects.filter(category=category).order_by('-views')  # Get pages in category
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    if request.user.is_authenticated:
        context_dict['user_liked'] = UserLike.objects.filter(user=request.user, category=category).exists()  # Check if user liked category
    else:
        context_dict['user_liked'] = False
    if request.method == 'POST':
        query = request.POST['query'].strip()  # Handle search query
        if query:
            context_dict['result_list'] = run_query(query)
            context_dict['query'] = query
    return render(request, 'rango/category.html', context=context_dict)

# Show page view
def show_page(request, category_name_slug, page_name_slug):
    context_dict = {}
    try:
        page = Page.objects.get(slug=page_name_slug)  # Get page by slug
        context_dict['page'] = page
        comments = page.comments.all()  # Get comments for the page
        context_dict['comments'] = comments
        if request.user.is_authenticated:
            context_dict['user_liked_page'] = UserLikePage.objects.filter(user=request.user, page=page).exists()  # Check if user liked page
        else:
            context_dict['user_liked_page'] = False
        recommended_dishes = RecommendedDish.objects.filter(page=page).values('dish_name').annotate(count=models.Count('dish_name')).order_by('-count')[:3]  # Get top 3 recommended dishes
        context_dict['recommended_dishes'] = recommended_dishes
        if request.method == 'POST':
            cmt_form = CommentForm(request.POST)
            dish_form = RecommendedDishForm(request.POST)
            price_form = PriceForm(request.POST)
            rating_form = RatingForm(request.POST)
            if cmt_form.is_valid():  # Handle comment form
                comment = cmt_form.save(commit=False)
                comment.page = page
                comment.user = request.user  
                comment.save()
                return redirect('rango:show_page', category_name_slug=category_name_slug, page_name_slug=page_name_slug)
            if dish_form.is_valid():  # Handle dish form
                recommended_dishes = dish_form.save(commit=False)
                recommended_dishes.page = page
                recommended_dishes.user = request.user  
                recommended_dishes.save()
                return redirect('rango:show_page', category_name_slug=category_name_slug, page_name_slug=page_name_slug)
            if price_form.is_valid():  # Handle price form
                price = price_form.save(commit=False)
                price.page = page
                price.user = request.user
                price.save()
                page.update_average_price()  # Update average price
                return redirect('rango:show_page', category_name_slug=category_name_slug, page_name_slug=page_name_slug)            
            if rating_form.is_valid():  # Handle rating form
                rating = rating_form.save(commit=False)
                rating.page = page
                rating.user = request.user
                rating.save()
                page.update_average_rating()  # Update average rating
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
        context_dict['title'] = None
        context_dict['page'] = None
        context_dict['comments'] = None
        context_dict['cmt_form'] = None
        context_dict['dish_form'] = None
        context_dict['price_form'] = None
        context_dict['rating_form'] = None
    return render(request, 'rango/page.html', context=context_dict)
    
# About page view
def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    return render(request, 'rango/about.html')
    
# Add category view
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
    
# Add page view
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)  # Get category by slug
    except Category.DoesNotExist:
        category = None
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
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
            else:
                print(form.errors)
    else:
        form = PageForm()
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

# Redirect to page URL
def goto_url(request):
    page_id = None
    if request.method == 'GET':
        page_id = request.GET.get('page_id')
        if page_id:
            try:            
                selected_page = Page.objects.get(id=int(page_id))  # Get page by ID
                selected_page.views = selected_page.views + 1  # Increment views
                category_slug = selected_page.category.slug
                page_slug = selected_page.slug
                selected_page.save()
            except selected_page.DoesNotExist:
                return redirect(reverse('rango:index'))
            return redirect(reverse('rango:show_page', kwargs={'category_name_slug': category_slug, 'page_name_slug': page_slug}))
    return redirect(reverse('rango:index'))

# Restricted view for logged-in users
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
   
# Get server-side cookie
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
    
# Handle visitor cookies
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

# Like category view
class LikeCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        category_id = request.GET.get('category_id')
        try:
            category = Category.objects.get(id=int(category_id))  # Get category by ID
        except (Category.DoesNotExist, ValueError):
            return HttpResponse(-1)  
        if UserLike.objects.filter(user=request.user, category=category).exists():
            return HttpResponse(-2)  
        UserLike.objects.create(user=request.user, category=category)
        category.likes += 1
        category.save()
        return HttpResponse(category.likes)
        
# Like page view
class LikePageView(View):
    @method_decorator(login_required)
    def get(self, request):
        page_id = request.GET.get('page_id')
        try:
            page = Page.objects.get(id=int(page_id))  # Get page by ID
        except (Page.DoesNotExist, ValueError):
            return HttpResponse(-1)  
        if UserLikePage.objects.filter(user=request.user, page=page).exists():
            return HttpResponse(-2)  
        UserLikePage.objects.create(user=request.user, page=page)
        page.likes += 1
        page.save()
        return HttpResponse(page.likes)

# Contact us view
def contact_us(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = ContactUs(full_name=full_name, email=email, subject=subject, message=message)
        contact.save()
        return render(request, 'rango/sucess.html')
    return render(request, 'rango/contact_us.html')