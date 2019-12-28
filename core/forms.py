from django import forms

PAYMENT_CHOICES = (
    ('CC','Credit Card'),
    ('DB', 'Debit Card'),
    ('OV', 'OVO'),
    )

COURIER_CHOICES =(
    ('JNE', 'JNE'),
    ('J&T', 'J&T'),
    ('TIKI', 'TIKI'),
)



SORT_CHOICES = (
    ('N', 'Nama'),
    ('HT', 'Harga Tertinggi'),
    ('HR', 'Harga Terendah'),
)

class CourierForm(forms.Form):
    courier = forms.ChoiceField(choices=COURIER_CHOICES)


class ItemQuantForm(forms.Form):
    quant = forms.IntegerField()


class CheckOutForm(forms.Form):
    address = forms.CharField(required=True)
    address2 = forms.CharField(required=False)
    phone_num = forms.CharField(required=True,max_length=14)
    zip = forms.CharField(required=True)
    # use_default_address = forms.BooleanField(required=True)
    set_default_address = forms.BooleanField(required=False)
    
class PaymentOptForm(forms.Form):
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(),choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    coupon = forms.CharField(required=False)


class SortForm(forms.Form):
    name = forms.ChoiceField(choices=SORT_CHOICES)