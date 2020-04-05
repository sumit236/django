from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone


def home(request):
    products = Product.objects
    return render(request, 'products/home.html', {'products': products})


@login_required
def create(request):
    if request.method == 'POST':
        # print all details of WSGIRequest in json
        print(request.__dict__)
        # _post or POST of request contains title body and _files or FILES of request contains image and icon
        if request.POST['title'] and request.POST['body'] and request.FILES['image'] and request.FILES['icon']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            product.image = request.FILES['image']
            product.icon = request.FILES['icon']
            product.pub_date = timezone.datetime.now()
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = "http://" + request.POST['url']
            # associates all the product to a single user.
            product.hunter = request.user
            # save to the producthunterdb db
            product.save()
            return redirect('home')

        else:
            return render(request, 'products/create.html', {'error': "All fields are required !!"})
    else:
        return render(request, 'products/create.html')


def details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/details.html', {'product': product})


@login_required(login_url='/accounts/signup')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/'+ str(product_id))
