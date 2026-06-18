document.addEventListener('DOMContentLoaded', function() {
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

    // اضافه کردن انیمیشن برای دکمه پرداخت (اختیاری)
    const payBtn = document.querySelector('.btn-pay');
    if (payBtn) {
        payBtn.addEventListener('click', function(e) {
            // فقط یک افکت ساده، بدون جلوگیری از ارسال
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 200);
        });
    }
});