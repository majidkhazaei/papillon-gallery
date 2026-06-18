document.addEventListener('DOMContentLoaded', function() {
    const removeLinks = document.querySelectorAll('.cart-simple-table a[href*="cart_remove"]');
    removeLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('آیا از حذف این محصول از سبد خرید مطمئن هستید؟')) {
                e.preventDefault();
            }
        });
    });
});