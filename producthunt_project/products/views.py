from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.datastructures import MultiValueDictKeyError
import datetime


# def home(request):
#     products = Product.objects
#     return render(request, 'products/home.html', {'products': products})


def home(request):
    products = Product.objects.all()
    print(">>>>>>>>>>>>>", products)
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'products/home.html', {'products': users})


def filterby_pub_date(request):
    # Sort the QuerySet object (containing list of product object) by pub_date in descending order ('-' indicates descending)
    products = Product.objects.all().order_by('-pub_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'products/home.html', {'products': users})


def filterby_upvote(request):
    # Sort the QuerySet object (containing list of product object) by upvote in descending order ('-' indicates descending)
    products = Product.objects.all().order_by('-votes_total')
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'products/home.html', {'products': users})


@login_required
def create(request):
    if request.method == 'POST':
        # print all details of WSGIRequest in json
        print(request.__dict__)
        # _post or POST of request contains title body and _files or FILES of request contains image and icon
        # if request.POST['title'] and request.POST['body'] and request.FILES['image'] and request.FILES['icon']:
        product = Product()
        # Validating the fields and Marking Title, Body, Icon as Mandatory else throw error.
        if request.POST['title']:
            product.title = request.POST['title']
        else:
            return render(request, 'products/create.html', {"error": "Title is mandatory"})
        # Validate Body field
        if request.POST['body']:
            product.body = request.POST['body']
        else:
            return render(request, 'products/create.html', {"error": "Some description is mandatory in Body section"})
        # Validate Image field
        product.image = request.FILES['image']
        product.pub_date = datetime.date.today()
        # Validate Icon field
        try:
            if request.FILES['icon']:
                product.icon = request.FILES['icon']
            else:
                return render(request, 'products/create.html', {"error": "Icon is mandatory"})
        except MultiValueDictKeyError:
            return render(request, 'products/create.html', {"error": "Icon is mandatory"})

        if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
            product.url = request.POST['url']
        else:
            product.url = "http://" + request.POST['url']
        # associates all the product to a single user.
        product.hunter = request.user
        print(">>>>>>>>>>>>>>>> testing", product)
        # save to the producthunterdb db
        product.save()
        return redirect('home')
    else:
        return render(request, 'products/create.html')


def details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/details.html', {'product': product})


@login_required(login_url='/accounts/login')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product_id))


def user_specific_posts(request, product_id):
    if request.method == 'GET':
        # returns an object if found else return None
        # product = get_object_or_404(Product, pk=product_id)
        # returns a QuerySet object with filter provided
        product = Product.objects.filter(pk=product_id)
        # fetch all the product associated with a single hunter/creator.
        product_list = Product.objects.filter(hunter=product[0].hunter)
        return render(request, 'products/user_specific_posts.html', {'product_list': product_list})
