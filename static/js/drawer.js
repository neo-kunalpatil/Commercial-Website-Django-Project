// Side Drawer (Hamburger Menu) logic
document.addEventListener('DOMContentLoaded', function() {
    const openBtn = document.getElementById('open-drawer-btn');
    const closeBtn = document.getElementById('close-drawer-btn');
    const drawerOverlay = document.querySelector('.drawer-overlay');
    const sideDrawer = document.querySelector('.side-drawer');

    function openDrawer(e) {
        if(e) e.preventDefault();
        drawerOverlay.classList.add('open');
        sideDrawer.classList.add('open');
        document.body.style.overflow = 'hidden'; // prevent background scrolling
    }

    function closeDrawer(e) {
        if(e) e.preventDefault();
        sideDrawer.classList.remove('open');
        setTimeout(() => {
            drawerOverlay.classList.remove('open');
            document.body.style.overflow = '';
        }, 300); // match CSS transition duration
    }

    if (openBtn) openBtn.addEventListener('click', openDrawer);
    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
    
    // Close on overlay click
    if (drawerOverlay) {
        drawerOverlay.addEventListener('click', function(e) {
            if (e.target === drawerOverlay) {
                closeDrawer();
            }
        });
    }
});
