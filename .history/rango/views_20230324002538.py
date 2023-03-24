# modification for registration
from django.conf import settings
from django.utils.module_loading import import_string

# original imports
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category
from rango.models import Page

from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm

from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from datetime import datetime

from rango.bing_search import run_query

REGISTRATION_FORM_PATH = getattr(settings, 'REGISTRATION_FORM',
                                 'registration.forms.RegistrationForm')
REGISTRATION_FORM = import_string(REGISTRATION_FORM_PATH)

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    
    visitor_cookie_handler(request)
    
    response = render(request, 'rango/index.html', context=context_dict)
    return response
    
def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Fangzheng Tian.'}
    
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    
    response = render(request, 'rango/about.html', context=context_dict)
    return response

def show_category(request, category_name_slug):
    context_dict = {}
    
    result_list = []
    value = ""
    
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')
        
        context_dict['pages'] = pages
        context_dict['category'] = category
    
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    
    # research function
    if request.method == 'POST':
        query = request.POST['query'].strip()
        value = query
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
    
    context_dict['result_list'] = result_list
    context_dict['value'] = value
        
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    
    if request.method == "POST":
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            cat = form.save(commit=True)
            print(cat, cat.slug)
            return redirect('/rango/')
        else:
            print(form.errors)
        
    return render(request, 'rango/add_category.html', {'form':form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
        
    if category is None:
        return redirect('/rango/')
    
    form = PageForm()
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))
            
        else:
            print(form.errors)
                
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
    
@login_required
def restricted(request):
    context_dict={'boldmessage':'Since you\'re logged in, you can see this text!'}
    return render(request, 'rango/restricted.html', context=context_dict)

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    # print("test")
    # for i in last_visit_cookie[:-7]:
    #     print(i)
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits
    
def search(request):
    
    context_dict = {}
    result_list = []
    value = ""
    
    if request.method == 'POST':
        query = request.POST['query'].strip()
        value = query
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
    
    context_dict['result_list'] = result_list
    context_dict['value'] = value
            
    return render(request, 'rango/search.html', context_dict)

def goto_url(request):
    
    if request.method == 'GET':
        page_id = request.GET.get('page_id')
        
        try:
            selected_page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return redirect(reverse('rango:index'))
        
        selected_page.views = selected_page.views + 1
        selected_page.save()
        
        return redirect(selected_page.url)
    
    return redirect(reverse('rango:index'))

@login_required
def register_profile(request):
    form = UserProfileForm()
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
            
        context_dict = {'form': form}
        return render(request, 'rango/profile_registration.html', context_dict)