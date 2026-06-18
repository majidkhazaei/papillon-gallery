document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('[data-dropdown]');

    function closeAllDropdowns(except = null) {
        dropdowns.forEach(d => {
            if (except !== d) d.classList.remove('open');
        });
    }

    function toggleDropdown(dropdown) {
        if (dropdown.classList.contains('open')) {
            dropdown.classList.remove('open');
        } else {
            closeAllDropdowns(dropdown);
            dropdown.classList.add('open');
        }
    }

    dropdowns.forEach(dropdown => {
        const btn = dropdown.querySelector('[data-dropdown-btn]');
        if (btn) {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                toggleDropdown(dropdown);
            });
        }
    });

    document.addEventListener('click', function(e) {
        let inside = false;
        dropdowns.forEach(d => { if (d.contains(e.target)) inside = true; });
        if (!inside) closeAllDropdowns();
    });
});
document.addEventListener('DOMContentLoaded', function() {

    // ===== DROPDOWN MENU (همان کد قبلی) =====
    const dropdowns = document.querySelectorAll('[data-dropdown]');

    function closeAllDropdowns(except = null) {
        dropdowns.forEach(d => {
            if (except !== d) d.classList.remove('open');
        });
    }

    function toggleDropdown(dropdown) {
        if (dropdown.classList.contains('open')) {
            dropdown.classList.remove('open');
        } else {
            closeAllDropdowns(dropdown);
            dropdown.classList.add('open');
        }
    }

    dropdowns.forEach(dropdown => {
        const btn = dropdown.querySelector('[data-dropdown-btn]');
        if (btn) {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                toggleDropdown(dropdown);
            });
        }
    });

    document.addEventListener('click', function(e) {
        let inside = false;
        dropdowns.forEach(d => { if (d.contains(e.target)) inside = true; });
        if (!inside) closeAllDropdowns();
    });

    // ===== IMAGE ZOOM MODAL (جدید) =====
    // ایجاد المان‌های مُدال به صورت داینامیک
    function createModal() {
        const modal = document.createElement('div');
        modal.className = 'image-modal';
        modal.id = 'imageModal';
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-modal', 'true');
        modal.innerHTML = `
            <button class="close-modal" id="closeModal" aria-label="بستن">✕</button>
            <img id="modalImage" src="" alt="بزرگنمایی تصویر">
            <div class="modal-info">
                <span class="name" id="modalName">نام اثر</span>
                <span class="price" id="modalPrice">قیمت</span>
            </div>
        `;
        document.body.appendChild(modal);
        return modal;
    }

    const modal = createModal();
    const modalImg = document.getElementById('modalImage');
    const modalName = document.getElementById('modalName');
    const modalPrice = document.getElementById('modalPrice');
    const closeBtn = document.getElementById('closeModal');

    // باز کردن مُدال با کلیک روی عکس
    document.querySelectorAll('.product-image').forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function(e) {
            e.stopPropagation();
            // پیدا کردن کارت محصول والد
            const card = this.closest('.product-card');
            const nameEl = card ? card.querySelector('.product-name a') : null;
            const priceEl = card ? card.querySelector('.product-price') : null;

            modalImg.src = this.src;
            modalImg.alt = this.alt;
            modalName.textContent = nameEl ? nameEl.textContent : 'بدون نام';
            modalPrice.textContent = priceEl ? priceEl.textContent : '';

            modal.classList.add('active');
            document.body.style.overflow = 'hidden'; // جلوگیری از اسکرول
        });
    });

    // بستن مُدال
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    // کلیک روی دکمه بستن
    closeBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        closeModal();
    });

    // کلیک روی پس‌زمینه مُدال (خود مُدال)
    modal.addEventListener('click', function(e) {
        if (e.target === this) {
            closeModal();
        }
    });

    // کلیک روی دکمه Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });

    // اگر روی عکس داخل مُدال کلیک شود، بسته نشود
    modalImg.addEventListener('click', function(e) {
        e.stopPropagation();
    });

    console.log('✅ Image zoom modal activated for ' + document.querySelectorAll('.product-image').length + ' products');
});