from django.shortcuts import redirect, render

# Create your views here.
def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')



from .models import UserRegister

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_pic = request.FILES.get('profile_pic')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        if UserRegister.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'Account already exists with this email.'
            })
        UserRegister.objects.create(
            name=name,
            email=email,
            password=password,
            profile_pic=profile_pic,
            age=age,
            phone=phone
           
        )

        return redirect('login')

    return render(request, 'register.html')

from django.shortcuts import render, redirect
from .models import UserRegister


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = UserRegister.objects.get(email=email)

            if user.password == password:
                # Add email to session
                request.session['email'] = user.email

                return redirect('home')  # change to your home URL name

            else:
                return render(request, "login.html", {
                    "error": "Invalid password"
                })

        except UserRegister.DoesNotExist:
            return render(request, "login.html", {
                "error": "Email not registered"
            })

    return render(request, "login.html")

from django.shortcuts import render, redirect
from .models import UserRegister


def profile(request):

    email = request.session.get('email')

    if not email:
        return redirect('login')

    user = UserRegister.objects.get(email=email)

    return render(request, "profile.html", {
        "user": user
    })

from django.shortcuts import render, redirect
from .models import UserRegister


def edit_profile(request):

    email = request.session.get('email')

    if not email:
        return redirect('login')


    user = UserRegister.objects.get(email=email)


    if request.method == "POST":

        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.age = request.POST.get('age')
        user.phone = request.POST.get('phone')


        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES.get('profile_pic')


        user.save()


        # update session email if email changed
        request.session['email'] = user.email


        return redirect('profile')


    return render(request, "edit_profile.html", {
        "user": user
    })

from django.shortcuts import render, redirect
from .models import UserRegister, Product

def add_product(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        product_image = request.FILES.get("product_image")

        # Get user email from session
        email = request.session.get("email")

        if not email:
            return redirect("login")

        try:
            user = UserRegister.objects.get(email=email)

            Product.objects.create(
                user=user,
                product_name=product_name,
                description=description,
                price=price,
                product_image=product_image
            )

            return redirect("product_list")  # change to your page

        except UserRegister.DoesNotExist:
            return redirect("login")

    return render(request, "add_product.html")

from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.select_related('user').all().order_by('-created_at')

    return render(request, "product_list.html", {
        "products": products
    })

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def my_products(request):
    user_id = request.session.get("email")

    if not user_id:
        return redirect("login")

    user = UserRegister.objects.get(email=user_id)
    products = Product.objects.filter(user=user).order_by("-created_at")

    return render(request, "my_products.html", {
        "products": products
    })

def delete_product(request, pk):
    user_id = request.session.get("email")
    user = UserRegister.objects.get(email=user_id)
    product = get_object_or_404(
        Product,
        id=pk,
        user=user
    )

    product.delete()

    return redirect("my_products")

def edit_product(request, pk):
    user_id = request.session.get("email")
    user = UserRegister.objects.get(email=user_id)

    product = get_object_or_404(
        Product,
        id=pk,
        user=user
    )

    if request.method == "POST":
        product.product_name = request.POST.get("product_name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")

        if request.FILES.get("product_image"):
            product.product_image = request.FILES.get("product_image")

        product.save()

        return redirect("my_products")

    return render(request, "edit_product.html", {
        "product": product
    })

from .models import Cart, Product, UserRegister
from django.shortcuts import redirect, render, get_object_or_404

def add_to_cart(request, pk):
    email = request.session.get("email")

    if not email:
        return redirect("login")

    user = UserRegister.objects.get(email=email)
    product = get_object_or_404(Product, id=pk)

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


def cart(request):
    email = request.session.get("email")

    if not email:
        return redirect("login")

    user = UserRegister.objects.get(email=email)

    cart_items = Cart.objects.filter(user=user).select_related("product")

    return render(request, "cart.html", {
        "cart_items": cart_items
    })

from django.shortcuts import redirect, get_object_or_404
from .models import Cart, UserRegister

def increase_quantity(request, pk):
    email = request.session.get("email")

    if not email:
        return redirect("login")

    user = UserRegister.objects.get(email=email)

    cart_item = get_object_or_404(
        Cart,
        id=pk,
        user=user
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect("cart")


def decrease_quantity(request, pk):
    email = request.session.get("email")

    if not email:
        return redirect("login")

    user = UserRegister.objects.get(email=email)

    cart_item = get_object_or_404(
        Cart,
        id=pk,
        user=user
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart")


def remove_from_cart(request, pk):
    email = request.session.get("email")

    if not email:
        return redirect("login")

    user = UserRegister.objects.get(email=email)

    cart_item = get_object_or_404(
        Cart,
        id=pk,
        user=user
    )

    cart_item.delete()

    return redirect("cart")

def cart(request):
    email = request.session.get("email")

    if not email:
        return redirect("login")

    user = UserRegister.objects.get(email=email)

    cart_items = Cart.objects.filter(user=user)

    grand_total = 0

    for item in cart_items:
        item.total = item.product.price * item.quantity
        grand_total += item.total

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "grand_total": grand_total
    })