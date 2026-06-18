from django import forms

class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9)
    size = forms.CharField(max_length=50)  


class CouponApplyForm(forms.Form):
    code = forms.CharField()


class AddressForm(forms.Form):
    receiver_name = forms.CharField(max_length=100, label='نام گیرنده', required=True)
    receiver_phone = forms.CharField(max_length=11, label='تلفن گیرنده', required=True)
    address = forms.CharField(widget=forms.Textarea, label='آدرس کامل', required=True)
    postal_code = forms.CharField(max_length=20, required=True, label='کد پستی')