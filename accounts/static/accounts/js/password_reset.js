document.addEventListener('DOMContentLoaded', function() {
    // اعتبارسنجی ساده برای فرم‌های reset
    const forms = document.querySelectorAll('.reset-card form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = this.querySelectorAll('input[type="text"], input[type="email"], input[type="password"]');
            let empty = false;
            inputs.forEach(input => {
                if (input.value.trim() === '') {
                    empty = true;
                    input.style.borderColor = '#b22222';
                } else {
                    input.style.borderColor = '#e8d5d5';
                }
            });
            if (empty) {
                e.preventDefault();
                alert('لطفاً تمام فیلدها را پر کنید.');
            }
        });
    });
});