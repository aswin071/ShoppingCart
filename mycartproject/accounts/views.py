from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product,CartItem,Cart

# Create your views here.

@login_required
def index(request):
    products_Home = Product.objects.all()
    return render(request, 'index.html', {'products_Home': products_Home})
    

def signup(request):
    form=CreateUserForm()

    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account Created Successfully')
            return redirect('login')
    context={'form':form}
    return render(request, 'signup.html', context)



def user_login(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username OR Password is Incorrect')
            
    
    context={}
    
    return render(request, 'login.html',context)

def user_logout(request):
    
    if 'user_id' in request.session:
        del request.session['user_id']

    logout(request)
    return redirect('login')


def ProductPage(request):
    products = Product.objects.all()
    return render(request, 'Product.html', {'products': products})


def addProduct(request):
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Product added successfully.')
      return redirect('products')
    else:
      print(form.errors)
      messages.error(request, 'Invalid input!!!')
      return redirect('addproduct')
  else:
    form = ProductForm()
    context = {
      'form':form,
    }
    return render(request, 'addproduct.html', context)


def deleteProduct(request, id):
  product = Product.objects.get(id=id)
  product.delete()
  messages.success(request, 'Product deleted successfully.')
  return redirect('products')

def editProduct(request, id):
  product = Product.objects.get(id=id)
  
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES, instance=product)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Product edited successfully.')
      return redirect('products')
    else:
      messages.error(request, 'Invalid input')
      
  form =   ProductForm(instance=product)
  context = {
    'form':form,
    'product':product,
  }
  return render(request, 'editProduct.html', context)


def cart(request):
    cart_items = CartItem.objects.all()
    total_quantity = sum(item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_quantity': total_quantity})


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')
