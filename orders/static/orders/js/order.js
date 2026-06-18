document.addEventListener('DOMContentLoaded', function() {

    // ===== فرم کد تخفیف =====
    const couponForm = document.querySelector('.coupon-form');
    if (couponForm) {
        couponForm.addEventListener('submit', function(e) {
            const input = this.querySelector('input[type="text"]');
            if (input && input.value.trim() === '') {
                e.preventDefault();
                alert('لطفاً کد تخفیف را وارد کنید.');
            }
        });
    }

    // ===== فرم آدرس =====
    const addressForm = document.querySelector('.address-section form');
    if (addressForm) {
        addressForm.addEventListener('submit', function(e) {
            const inputs = this.querySelectorAll('input[type="text"], textarea');
            let isEmpty = false;
            inputs.forEach(input => {
                if (input.value.trim() === '') {
                    isEmpty = true;
                    input.style.borderColor = '#b22222';
                } else {
                    input.style.borderColor = '';
                }
            });
            if (isEmpty) {
                e.preventDefault();
                alert('لطفاً تمام فیلدهای آدرس را پر کنید.');
            }
        });
    }

    // ===== دکمه پرداخت =====
    const payBtn = document.querySelector('.btn-pay');
    if (payBtn) {
        payBtn.addEventListener('click', function(e) {
            // فقط یک افکت ساده
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 200);
        });
    }

    // ===== دکمه ویرایش آدرس =====
    const editBtn = document.querySelector('.btn-warning');
    if (editBtn) {
        editBtn.addEventListener('click', function(e) {
            if (!confirm('آیا می‌خواهید آدرس را ویرایش کنید؟')) {
                e.preventDefault();
            }
        });
    }
});