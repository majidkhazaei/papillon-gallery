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