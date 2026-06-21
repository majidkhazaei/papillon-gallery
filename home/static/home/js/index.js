document.addEventListener('DOMContentLoaded', function() {

    // ===== DROPDOWN MENU =====
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

    // ===== IMAGE ZOOM MODAL =====
    function createModal() {
        const modal = document.createElement('div');
        modal.className = 'image-modal';
        modal.id = 'imageModal';
        modal.innerHTML = `
            <button class="close-modal" id="closeModal">✕</button>
            <img id="modalImage" src="" alt="بزرگنمایی">
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

    document.querySelectorAll('.product-image').forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function(e) {
            e.stopPropagation();
            const card = this.closest('.product-card');
            const nameEl = card ? card.querySelector('.product-name a') : null;
            const priceEl = card ? card.querySelector('.product-price') : null;

            modalImg.src = this.src;
            modalImg.alt = this.alt;
            modalName.textContent = nameEl ? nameEl.textContent : 'بدون نام';
            modalPrice.textContent = priceEl ? priceEl.textContent : '';

            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });

    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    closeBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        closeModal();
    });

    modal.addEventListener('click', function(e) {
        if (e.target === this) closeModal();
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });

    modalImg.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});