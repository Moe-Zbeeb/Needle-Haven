document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-links li a');

    // Set default category to 'Womenswear' on page load
    setCategory('women');

    navLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default link behavior

            // Remove active class from all links
            navLinks.forEach(link => link.classList.remove('active'));

            // Add active class to the clicked link
            this.classList.add('active');

            // Set the selected category and update dropdowns
            setCategory(this.id);
        });
    });
});

let selectedCategory = '';

function setCategory(category) {
    selectedCategory = category;
    updateDropdowns();
}

function updateDropdowns() {
    const newInDropdown = document.getElementById('new-in-dropdown');
    const brandsDropdown = document.getElementById('brands-dropdown');
    const clothingDropdown = document.getElementById('clothing-dropdown');
    const shoesDropdown = document.getElementById('shoes-dropdown');
    const accessoriesDropdown = document.getElementById('accessories-dropdown');
    const saleDropdown = document.getElementById('sale-dropdown');

    // Clear previous content
    newInDropdown.innerHTML = '';
    brandsDropdown.innerHTML = '';
    clothingDropdown.innerHTML = '';
    shoesDropdown.innerHTML = '';
    accessoriesDropdown.innerHTML = '';
    saleDropdown.innerHTML = '';

    // Populate dropdowns based on selected category
    if (selectedCategory === 'women') {
        clothingDropdown.innerHTML = `
            <a href="#">Dresses</a>
            <a href="#">Tops & Blouses</a>
            <a href="#">T-shirts & Tanks</a>
            <a href="#">Sweaters & Cardigans</a>
            <a href="#">Jackets & Coats</a>
            <a href="#">Pants & Leggings</a>
            <a href="#">Skirts</a>
            <a href="#">Shorts</a>
            <a href="#">Jeans</a>
            <a href="#">Suits & Blazers</a>
            <a href="#">Activewear</a>
            <a href="#">Swimwear</a>
        `;
        shoesDropdown.innerHTML = `
            <a href="#">Heels</a>
            <a href="#">Flats</a>
            <a href="#">Boots</a>
            <a href="#">Sneakers</a>
            <a href="#">Sandals</a>
        `;
        accessoriesDropdown.innerHTML = `
            <a href="#">Bags</a>
            <a href="#">Belts</a>
            <a href="#">Hats</a>
            <a href="#">Jewelry</a>
            <a href="#">Scarves</a>
        `;
    } else if (selectedCategory === 'men') {
        clothingDropdown.innerHTML = `
            <a href="#">T-Shirts & Polos</a>
            <a href="#">Shirts</a>
            <a href="#">Sweaters & Hoodies</a>
            <a href="#">Jackets & Coats</a>
            <a href="#">Suits & Blazers</a>
            <a href="#">Pants & Chinos</a>
            <a href="#">Jeans</a>
            <a href="#">Shorts</a>
            <a href="#">Activewear</a>
            <a href="#">Swimwear</a>
        `;
        shoesDropdown.innerHTML = `
            <a href="#">Boots</a>
            <a href="#">Sneakers</a>
            <a href="#">Loafers</a>
            <a href="#">Oxfords</a>
            <a href="#">Sandals</a>
        `;
        accessoriesDropdown.innerHTML = `
            <a href="#">Bags</a>
            <a href="#">Belts</a>
            <a href="#">Hats</a>
            <a href="#">Watches</a>
            <a href="#">Sunglasses</a>
        `;
    } else if (selectedCategory === 'kids') {
        clothingDropdown.innerHTML = `
            <a href="#">Tops</a>
            <a href="#">Pants</a>
            <a href="#">Dresses</a>
            <a href="#">Outerwear</a>
            <a href="#">Swimwear</a>
        `;
        shoesDropdown.innerHTML = `
            <a href="#">Sneakers</a>
            <a href="#">Boots</a>
            <a href="#">Sandals</a>
            <a href="#">School Shoes</a>
        `;
        accessoriesDropdown.innerHTML = `
            <a href="#">Hats</a>
            <a href="#">Bags</a>
            <a href="#">Scarves</a>
            <a href="#">Gloves</a>
        `;
    }
}

// Function to open the sidebar
function openNav() {
    document.getElementById("mySidebar").style.width = "1000px";
    document.getElementById("overlay").style.display = "block";
}

// Function to close the sidebar
function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("overlay").style.display = "none";
}

// Function to show the selected tab in the sidebar
function showTab(tab) {
    document.getElementById('items-tab').classList.remove('active');
    document.getElementById('stores-tab').classList.remove('active');
    document.getElementById(tab + '-tab').classList.add('active');
}

// Close the sidebar if the user clicks outside of it
window.onclick = function(event) {
    if (event.target == document.getElementById("overlay")) {
        closeNav();
    }
}
