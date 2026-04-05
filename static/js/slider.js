// Horizontal Slider logic 
document.addEventListener('DOMContentLoaded', function() {
    // If custom horizontal scrolling is needed for product strips
    const strips = document.querySelectorAll('.horizontal-strip');
    
    strips.forEach(strip => {
        let isDown = false;
        let startX;
        let scrollLeft;

        strip.addEventListener('mousedown', (e) => {
            isDown = true;
            strip.style.cursor = 'grabbing';
            startX = e.pageX - strip.offsetLeft;
            scrollLeft = strip.scrollLeft;
        });
        
        strip.addEventListener('mouseleave', () => {
            isDown = false;
            strip.style.cursor = 'grab';
        });
        
        strip.addEventListener('mouseup', () => {
            isDown = false;
            strip.style.cursor = 'grab';
        });
        
        strip.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - strip.offsetLeft;
            const walk = (x - startX) * 2; // Scroll-fast
            strip.scrollLeft = scrollLeft - walk;
        });
    });
});
