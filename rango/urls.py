from django.urls import path
from rango import views, auth

app_name = 'rango'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
    path('category/<slug:category_name_slug>/',
         views.show_category, name='show_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('category/<slug:category_name_slug>/<slug:page_name_slug>/',
        views.show_page, name='show_page'),
    path('add_category/', views.add_category, name='add_category'),

    # Registration page
    path('register/', auth.register, name='register'),
    # Landing page
    path('login/', auth.user_login, name='login'),
    #Log out of the page
    path('logout/', auth.user_logout, name='logout'),
    # Change password page
    path('change_password/', auth.change_password, name='change_password'),
    #Edit the user profile page
    path('edit_profile/', auth.edit_profile, name='edit_profile'),
    
    path('restricted/', views.restricted, name='restricted'),
    #path('search/', views.search, name='search'),
    path('goto/', views.goto_url, name='goto'),
    path('like_category/', views.LikeCategoryView.as_view(), name='like_category'),
    path('like_page/', views.LikePageView.as_view(), name='like_page'),

    path('contact/', views.contact_us, name='contact'),
]