document.addEventListener('DOMContentLoaded', (event) => {
    const texts = ["EMPOWER", "FASHION", "STYLE", "UNIQUE", "GROWTH"];
    let index = 0;
    const changeText = () => {
        const textElement = document.getElementById('changingText');
        textElement.textContent = texts[index];
        index = (index + 1) % texts.length;
    };
    changeText();
    setInterval(changeText, 800); // Change text every 0.8 seconds
});


document.addEventListener("DOMContentLoaded", function() {
    const page3 = document.getElementById("page3");
    const leftSection = page3.querySelector(".left-section");
    const rightSection = page3.querySelector(".right-section");

    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observerCallback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                leftSection.classList.add("show");
                rightSection.classList.add("show");
            } else {
                leftSection.classList.remove("show");
                rightSection.classList.remove("show");
            }
        });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);
    observer.observe(page3);

    // Add click event listeners for each figure
    const figures = page3.querySelectorAll("figure");
    figures.forEach(figure => {
        figure.addEventListener("click", () => {
            figure.classList.toggle("active");
        });
    });
});

document.getElementById('contactButton').addEventListener('click', function() {
    document.getElementById('contactSection').scrollIntoView({ behavior: 'smooth' });
});

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
