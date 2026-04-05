// Navbar specific interactions
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.querySelector('.search-belt');
    const searchInput = document.querySelector('.search-belt input');

    if(searchInput) {
        searchInput.addEventListener('focus', function() {
            searchForm.style.boxShadow = '0 0 0 3px #f90';
        });
        
        searchInput.addEventListener('blur', function() {
            searchForm.style.boxShadow = 'none';
        });
    }
});
