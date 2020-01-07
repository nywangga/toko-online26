from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import ListView,DetailView,View
from .forms import ItemQuantForm,CheckOutForm, CouponForm,PaymentOptForm,CourierForm, SortForm
from .models import Item,OrderItem,Order,Address,Coupon, Courier
from django.core.paginator import Paginator
from django.db.models import Q


from midtransclient import Snap, CoreApi
import datetime


# @login_required
# def add_many_to_cart(request,slug):
#     item = get_object_or_404(Item, slug=slug)
#     form = ItemQuantForm(request.POST or None)
#     print(item)
#     if form.is_valid():
#         quant = form.cleaned_data.get('quant')
#         print(quant)
#         order_item,created = OrderItem.objects.get_or_create(
#             user = request.user,
#             ordered = False,
#             item = item,
#         )
#         order_qs = Order.objects.filter(
#             user = request.user,
#             ordered=False,
#         )
#         if order_qs.exists():
#             order = order_qs[0]
#             if order.items.filter(item__slug=item.slug).exists():
#                 order_item.quantity += quant
#                 order_item.save()
#                 messages.info(request, "This item was added to your cart")
#                 return redirect("core:product", slug=slug)
#             else:
#                 order_item.quantity = quant
#                 order_item.save()
#                 order.items.add(order_item)
#                 messages.info(request, "This item was added to your cart")
#                 return redirect("core:product", slug=slug)
#         else:
#             order_item.quantity = quant
#             order_item.save()
#             ordered_date = timezone.now()
#             order = Order.objects.create(user=request.user, ordered_date=ordered_date)
#             order.items.add(order_item)
#             messages.info(request, "This item was added to your cart")
#             return redirect("core:product", slug=slug)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created =OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect("core:order-summary")

        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart")
            return redirect("core:product",slug=slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
        return redirect("core:product", slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.filter(
        item=item,
        user=request.user,
        ordered=False
    )[0]
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity = 1
            order_item.save()
            order.items.remove(order_item)
            messages.info(request, "This item removed from cart")
            return redirect("core:order-summary")


        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)

    else:
        messages.info(request, "Your cart is empty")
        return redirect("core:product", slug=slug)


@login_required
def remove_one_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.filter(
        item=item,
        user=request.user,
        ordered=False
    )[0]
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity decreased")
            return redirect("core:order-summary")

        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product",slug=slug)

    else:
        messages.info(request, "Your cart is empty")
        return redirect("core:product", slug=slug)



class HomeView(ListView):
    paginate_by = 2
    def get(self, *args, **kwargs):
        item = Item.objects.all()
        courier = SortForm()
        context = {
            'courier':courier,
            'object_list':item
        }
        return render(self.request, 'home.html', context )


class SearchResultsView(ListView):

    model = Item
    template_name = 'search-results.html'
    # queryset = Item.objects.filter(title__icontains='Baju')

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(
            Q(title__icontains=query)|Q(category__icontains=query)
            )
        return object_list

class SortResultsView(ListView):

    def get(self, *args, **kwargs):
        query = self.request.GET.get('s')
        if query == 'N':
            item = Item.objects.order_by('title')
        elif query == 'HT':
            item = Item.objects.order_by('-price')
        else:
            item = Item.objects.order_by('price')
        form = SortForm()

        context = {
            'form':form,
            'object_list':item
        }
        return render(self.request, 'sort-results.html', context )
        
    # def get_queryset(self):
    #     query = self.request.GET.get('s')
    #     if query == 'N':
    #         return Item.objects.order_by('title')
    #     elif query == 'HT':
    #         return Item.objects.order_by('-price')
    #     else:
    #         return Item.objects.order_by('price')

    # def get(self, request, *args, **kwargs):
    #     return HttpResponse('GET request!')

    # def post(self, request, *args, **kwargs):
    #     return HttpResponse('POST request!')

class AddCouponView(View):
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        coupon = CouponForm(self.request.POST or None)
        if coupon.is_valid():
            try:
                coupon_name = coupon.cleaned_data.get('coupon')
                my_coupon = Coupon.objects.get(name=coupon_name)
                if my_coupon:
                    order.coup = my_coupon
                    order.save()
                    messages.info(self.request, 'Coupon added')
                    return redirect('core:checkout')
            except ObjectDoesNotExist:
                messages.info(self.request, 'Coupon does not exists')
                return redirect('core:checkout')

class DelCouponView(View):
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        order.coup = None
        order.save()
        messages.info(self.request, 'Coupon removed')
        return redirect('core:checkout')


class AddCourier(View):
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        courier = CourierForm(self.request.POST or None)
        if courier.is_valid():
            courier_name = courier.cleaned_data.get('courier')
            print(courier_name)
            if courier_name== 'JNE':
                courier_chosen ,created = Courier.objects.get_or_create(
                    name = courier_name,
                    amount = 9000,
                )
            elif courier_name== 'J&T':
                courier_chosen ,created = Courier.objects.get_or_create(
                    name = courier_name,
                    amount = 10000,
                )    
            elif courier_name== 'TIKI':
                courier_chosen ,created = Courier.objects.get_or_create(
                    name = courier_name,
                    amount = 11000,
                )
            order.courier = courier_chosen
            order.save()
            courier_chosen.save()
            return redirect('core:cekout')

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            addre = Address.objects.filter(user=self.request.user, default = True,)
            if addre.exists():
                addr = addre[0]
                courier = CourierForm()
                order = Order.objects.get(user=self.request.user, ordered=False)
                form = PaymentOptForm()
                coupon = CouponForm()
                context = {
                    'order':order,
                    'form':form,
                    'coupon': coupon,
                    'addr': addr,
                    'courierer':courier,
                    }
                return render(self.request, 'checkout.html', context)
            else:
                messages.info(self.request, 'tolong buat alamat terlebih dahulu')
                return redirect('core:address')
        except ObjectDoesNotExist:
            messages.info(self.request, 'No active order')
            return redirect('/')
    
    # def post(self, *args, **kwargs):
    #     form = PaymentOptForm(self.request.POST or None)
    #     try:
    #         if form.is_valid():
    #             payment_option = form.cleaned_data.get('payment_option')
    #             if payment_option == 'CC':
    #                 return redirect('core:payment',payment_option='cc')
    #             elif payment_option == 'DB':
    #                 return redirect('core:payment',payment_option='db')
    #             elif payment_option == 'OV':
    #                 return redirect('core:payment',payment_option='ovo')

    #     except ObjectDoesNotExist:
    #         messages.error(self.request, 'You have no active order')
    #         return redirect('core:checkout')

class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'payment.html')

    # def post(self, request, *args, **kwargs):
    #     return HttpResponse('POST request!')


class ProductView(DetailView):
    # model = Item
    # template_name = 'product.html'
    def get(self, request, slug, *args, **kwargs):
        form = ItemQuantForm()
        item = get_object_or_404(Item, slug=slug)
        context = {
            'object':item,
            'form':form
        }
        return render(self.request, 'product.html', context)

    def post(self, request,slug, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/accounts/login")

        else:
            item = get_object_or_404(Item, slug=slug)
            form = ItemQuantForm(self.request.POST or None)
            print(item)
            if form.is_valid():
                quant = form.cleaned_data.get('quant')
                print(quant)
                order_item,created = OrderItem.objects.get_or_create(
                    user = self.request.user,
                    ordered = False,
                    item = item,
                )
                order_qs = Order.objects.filter(
                    user = self.request.user,
                    ordered=False,
                )
                if order_qs.exists():
                    order = order_qs[0]
                    if order.items.filter(item__slug=item.slug).exists():
                        order_item.quantity += quant
                        order_item.save()
                        messages.info(request, "This item was added to your cart")
                        return redirect("core:product", slug=slug)
                    else:
                        order_item.quantity = quant
                        order_item.save()
                        order.items.add(order_item)
                        messages.info(request, "This item was added to your cart")
                        return redirect("core:product", slug=slug)
                else:
                    order_item.quantity = quant
                    order_item.save()
                    ordered_date = timezone.now()
                    order = Order.objects.create(user=request.user, ordered_date=ordered_date)
                    order.items.add(order_item)
                    messages.info(request, "This item was added to your cart")
                    return redirect("core:product", slug=slug)
                



class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context={
                'object': order
            }
            print(self.request)
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'order does not exist')
            return redirect('/')

    


class AddressView(View):
    def get(self, *args, **kwargs):
        form = CheckOutForm()
        address_qs = Address.objects.filter(
                    user=self.request.user)
        context = {
            'form':form,
            'address':address_qs,
        }
        return render(self.request, 'address.html', context)


    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        order = Order.objects.get(user=self.request.user, ordered=False)
        if form.is_valid():
            print('valid form')
            address_1 = form.cleaned_data.get('address')
            address_2 = form.cleaned_data.get('address2')
            zip = form.cleaned_data.get('zip')
            phone_num = form.cleaned_data.get('phone_num')
            address = Address(
                user=self.request.user,
                address= address_1,
                address2= address_2,
                phone = phone_num,
                zip = zip,
            )
            address.save()
            
            set_default = form.cleaned_data.get('set_default_address')
            if set_default:
                address_qs = Address.objects.filter(
                user=self.request.user,
                default = True,
                )
                if address_qs.exists():
                    for add in address_qs:
                        add.default = False
                        add.save()
                address.default = True
                address.save()
            order.address = address
            order.save()
            return redirect("core:checkout")
        else:
            messages.info(self.request, 'Insert the required fields')
            return redirect("core:address")



def set_def_address(request, pk):
    order = Order.objects.get(user=request.user, ordered=False)
    curr_add = Address.objects.get(pk=pk)
    address_qs = Address.objects.filter(
        user=request.user,
        default = True,
        )
    if address_qs.exists():
        for add in address_qs:
            add.default = False
            add.save()
    # curr_add.default = True
    order.address = curr_add
    order.address.default = True
    curr_add.save()
    order.save()
    return redirect("core:address")


def del_address(request, pk):
    curr_add = Address.objects.get(pk=pk)
    curr_add.delete()
    return redirect("core:address")



def simple_checkout(request):
    order = Order.objects.get(user=request.user, ordered=False)
    snap = Snap(
        is_production=False,
        server_key='SB-Mid-server-8oJZqmeP0EVRpxNGG7pLNldc',
        client_key='SB-Mid-client-EGD425osvvKZSWw7',
    )
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction_token = snap.create_transaction_token({
        "transaction_details": {
            "order_id": "order-id-python-"+timestamp,
            "gross_amount": order.get_fin_total()
        }, "credit_card":{
            "secure" : True
        }
    })
    order_id =  "order-id-python-"+timestamp
    order.iden = order_id
    order.save()
    context = {
        'token': transaction_token,
        'client_key' : snap.api_config.client_key,
        'order': order
    }
    
    return render(request, 'payment.html', context)


def update_transaction(request):
    order = Order.objects.get(user=request.user, ordered=False)
    snap = Snap(
        is_production=False,
        server_key='SB-Mid-server-8oJZqmeP0EVRpxNGG7pLNldc',
        client_key='SB-Mid-client-EGD425osvvKZSWw7',
    )
    status_response = snap.transactions.status(order.iden)
    print(status_response)
    order_id = status_response['order_id']
    transaction_status = status_response['transaction_status']
    fraud_status = status_response['fraud_status']

    print('Transaction notification received. Order ID: {0}. Transaction status: {1}. Fraud status: {2}'.format(order_id,
            transaction_status,
            fraud_status))

    # Sample transaction_status handling logic

    if transaction_status == 'capture':
        if fraud_status == 'challenge':
            # TODO set transaction status on your databaase to 'challenge'
            None

        elif fraud_status == 'accept':
            # TODO set transaction status on your databaase to 'success'
            order.ordered = True
            order.save()
            return render(request, 'update.html', {'order':order})
    elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
        # TODO set transaction status on your databaase to 'failure'
        None
    elif transaction_status == 'pending':
        # TODO set transaction status on your databaase to 'pending' / waiting payment
        None
