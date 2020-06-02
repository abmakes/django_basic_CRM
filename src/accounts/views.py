from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
# Create your views here.
from .models import *
from .forms import OrderForm

def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {'orders': orders, 'customers': customers,
    'total_orders':total_orders, 'delivered':delivered,
    'pending':pending}
    
    return render(request, "accounts/dashboard.html", context)
    
def products(request):
    products = Product.objects.all()

    return render(request, "accounts/products.html", {'products': products})
    
def customer(request, pk):
    customerA = Customer.objects.get(id=pk)

    orders = customerA.order_set.all()
    order_count = orders.count()    

    context = {'customer':customerA, 'orders':orders, 'order_count':order_count}
    return render(request, "accounts/customer.html", context)

def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=5)
    customerA = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customerA)
    #form = OrderForm(initial={'customer':customerA})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customerA)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, "accounts/order_form.html", context)

def updateOrder(request, pk):

    order= Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, "accounts/order_form.html", context)

def deleteOrder(request, pk):
    
    order= Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, "accounts/delete.html", context)