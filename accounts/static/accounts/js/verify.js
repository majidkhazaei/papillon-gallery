document.addEventListener('DOMContentLoaded', function() {
    let timeLeft = 120;
    const timerDisplay = document.getElementById('countdown');
    const resendBtn = document.getElementById('resend-btn');
    let timerInterval = null;

    function formatTime(s) {
        const m = Math.floor(s / 60);
        const sec = s % 60;
        return `${m.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`;
    }

    function startTimer() {
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(() => {
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                timerDisplay.textContent = '00:00';
                resendBtn.disabled = false;
            } else {
                timeLeft--;
                timerDisplay.textContent = formatTime(timeLeft);
            }
        }, 1000);
    }

    function resetTimer() {
        timeLeft = 120;
        timerDisplay.textContent = formatTime(timeLeft);
        resendBtn.disabled = true;
        if (timerInterval) clearInterval(timerInterval);
        startTimer();
    }

    resendBtn.addEventListener('click', function() {
        if (resendBtn.disabled) return;
        fetch(resendUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(r => r.json())
        .then(data => {
            if (data.status === 'ok') {
                alert('کد جدید ارسال شد.');
                resetTimer();
            } else {
                alert('خطا در ارسال مجدد کد.');
            }
        })
        .catch(() => alert('مشکل در ارتباط با سرور.'));
    });

    startTimer();
});