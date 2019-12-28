from django.db import models
from django.conf import settings
from django.urls import reverse

CATEGORY_CHOICES=(
    ('B', 'Baju'),
    ('C','Celana'),
    ('S','Sepatu'),
    )

LABEL_CHOICES=(
    ('D', 'danger'),
    ('P','primary'),
    ('S','secondary'),
    )

User = settings.AUTH_USER_MODEL

class Item(models.Model):
    title = models.CharField(max_length = 40)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    slug = models.SlugField()
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:product', kwargs={
            'slug': self.slug
            })

    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart', kwargs={'slug': self.slug})
    
    def remove_from_cart_url(self):
        return reverse('core:remove-from-cart', kwargs={'slug': self.slug})
    
    def remove_one_from_cart_url(self):
        return reverse('core:remove-one-from-cart', kwargs={'slug': self.slug})

    def add_x_to_cart(self):
        return reverse('core:product', kwargs={'slug': self.slug})

class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'

    def get_total_price(self):
        if not self.item.discount_price:
            return self.item.price * self.quantity
        else:
            return self.item.discount_price * self.quantity

    # def get_total_price_after_discount(self):
    #     return self.get_total_price() - (self.quantity * self.item.discount_price)

    def discount_saved(self):
        return self.get_total_price()


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    address = models.ForeignKey('Address', on_delete=models.SET_NULL,blank=True, null=True)
    coup = models.ForeignKey('Coupon', on_delete=models.SET_NULL,blank=True, null=True)
    courier = models.ForeignKey('Courier', on_delete=models.SET_NULL,blank=True, null=True)
    iden = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

    

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        if self.coup:
            return total - int(total * self.coup.amount / 100)
        else:
            return total
    
    def coup_disc(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        return int(total * self.coup.amount / 100)

    def item_quantity(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.quantity
        return total

    def get_fin_total(self):
        return self.get_total() + self.courier.amount


class Address(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    zip = models.CharField(max_length=6)
    default = models.BooleanField(default=False)
    phone = models.CharField(max_length=14)

    def __str__(self):
        return self.address[:10]

    def get_absolute_url(self):
        return reverse('core:set-default-address', kwargs={
            'pk': self.pk
            })

    def delete_address(self):
        return reverse('core:delete-address', kwargs={
            'pk': self.pk
            })
    # def __unicode__(self):
    #     return 


class Coupon(models.Model):
    name = models.CharField(max_length = 15)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Courier(models.Model):
    name = models.CharField(max_length = 7)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


