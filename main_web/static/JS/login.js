window.addEventListener('scroll', function() {
    const headerRight = document.querySelector('.header-right');
    const scrollY = window.scrollY || document.documentElement.scrollTop;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;

    // Calculate the percentage of the page that has been scrolled
    const scrollPercentage = scrollY / maxScroll;

    // Calculate the new width based on the scroll percentage
    const minWidth = 205; // Initial width in pixels
    const maxWidth = window.innerWidth; // Full width
    const newWidth = minWidth + (maxWidth - minWidth) * scrollPercentage;

    // Set the new width of the header-right
    headerRight.style.width = `${newWidth}px`;
});