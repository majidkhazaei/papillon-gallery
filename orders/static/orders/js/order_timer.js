// order_timer.js
document.addEventListener('DOMContentLoaded', function() {
    const timerElement = document.getElementById('order-timer');
    if (!timerElement) return; // اگر المنت وجود نداشت، کاری نکن

    // دریافت زمان ایجاد سفارش از دیتا-اتریبیوت
    const createdTime = new Date(timerElement.dataset.created).getTime();
    const now = new Date().getTime();
    let timeLeft = 600 - Math.floor((now - createdTime) / 1000); // 600 ثانیه = ۱۰ دقیقه

    const payButton = document.querySelector('.btn-pay');

    function updateTimer() {
        if (timeLeft <= 0) {
            timerElement.textContent = '00:00';
            if (payButton) {
                payButton.disabled = true;
                payButton.textContent = '⏳ زمان به پایان رسید';
                payButton.classList.add('btn-secondary');
                payButton.classList.remove('btn-success');
            }
            // می‌تونی پیام هشدار هم بدی
            // alert('زمان شما به پایان رسید. لطفاً دوباره سفارش دهید.');
            // یا صفحه رو رفرش کنی:
            // location.reload();
            return;
        }

        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent =
            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        timeLeft--;
    }

    // اجرای اولیه
    updateTimer();
    // آپدیت هر ثانیه
    setInterval(updateTimer, 1000);
});