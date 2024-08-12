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

document.addEventListener('DOMContentLoaded', () => {
    const tripleBubbles = 4; // Number of bubbles created per interval
    const maxBubbles = 40;

    const createBubble = () => {
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.classList.add(Math.random() < 0.25 ? 'green' : Math.random() < 0.5 ? 'pink' : Math.random() < 0.75 ? 'blue' : 'yellow');
        const size = Math.random() * 60 + 20;
        bubble.style.width = `${size}px`;
        bubble.style.height = `${size}px`;

        // Ensure bubbles appear only on the left (0-20%) or right (80-100%) sides of the page
        const isLeftSide = Math.random() < 0.5;
        const leftPosition = isLeftSide ? Math.random() * 20 : 80 + Math.random() * 20;
        bubble.style.left = `${leftPosition}%`;

        bubble.style.animationDuration = `${Math.random() * 10 + 20}s`; // Increase duration to slow down the bubbles
        return bubble;
    };

    const addBubblesToPage = (page) => {
        const bubbleContainer = document.createElement('div');
        bubbleContainer.className = 'bubble-container';

        page.appendChild(bubbleContainer);

        setInterval(() => {
            for (let i = 0; i < tripleBubbles; i++) {
                if (bubbleContainer.children.length >= maxBubbles) {
                    bubbleContainer.removeChild(bubbleContainer.children[0]); // Remove the oldest bubble
                }
                const bubble = createBubble();
                bubbleContainer.appendChild(bubble);
            }
        }, 3000); // Very short interval for continuous creation of bubbles
    };

    // Apply the bubble effect to pages from page4 to page1
    const pages = ['page4', 'page3', 'page2', 'page1'];
    pages.forEach(pageId => {
        const page = document.getElementById(pageId);
        if (page) {
            console.log(`Adding bubbles to ${pageId}`);
            addBubblesToPage(page);
        } else {
            console.log(`Page ${pageId} not found`);
        }
    });
});


function openNav() {
    document.getElementById("mySidebar").style.width = "1000px";
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
}

function showTab(tab) {
    document.getElementById('items-tab').classList.remove('active');
    document.getElementById('stores-tab').classList.remove('active');
    document.getElementById(tab + '-tab').classList.add('active');
}
