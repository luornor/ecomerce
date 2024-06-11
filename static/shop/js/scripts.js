
document.addEventListener('DOMContentLoaded', function () {
    fetchCategories();
    fetchRegions();
    fetchProducts();
    fetchCart();
});


function fetchCategories() {
    fetch('/api/categories/')
        .then(response => response.json())
        .then(data => {
            const categorySelect = document.getElementById('filter-category');
            categorySelect.innerHTML = '<option value="">All Categories</option>';
            data.forEach(category => {
                const option = document.createElement('option');
                option.value = category.id;
                option.textContent = category.name;
                categorySelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching categories:', error));
}

function fetchRegions() {
    fetch('/api/regions/')
        .then(response => response.json())
        .then(data => {
            const regionSelect = document.getElementById('filter-region');
            regionSelect.innerHTML = '<option value="">All Regions</option>';
            data.forEach(region => {
                const option = document.createElement('option');
                option.value = region.id;
                option.textContent = region.name;
                regionSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching regions:', error));
}

function fetchProducts(filters = {}) {
    let url = '/api/products';
    const params = new URLSearchParams(filters).toString();
    if (params) {
        url += `?${params}`;
    }
    console.log(params)

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            const productList = document.getElementById('product-list');
            productList.innerHTML = '';
            data.forEach(product => {
                const col = document.createElement('div');
                col.className = 'col-md-4';
                col.innerHTML = `
                    <div class="card mb-4">
                        <img src="${product.image_url}" class="card-img-top" alt="${product.name}">
                        <div class="card-body">
                            <h5 class="card-title">${product.name}</h5>
                            <p class="card-text">${product.description}</p>
                            <p class="card-text">$${product.price}</p>
                            <button class="btn btn-primary" onclick="addToCart(${product.id})">Add to Cart</button>
                        </div>
                    </div>
                `;
                productList.appendChild(col);
            });
        })
        .catch(error => console.error('Error fetching products:', error));
}

function applyFilters() {
    const category = document.getElementById('filter-category').value;
    const region = document.getElementById('filter-region').value;
    const minPrice = document.getElementById('filter-min-price').value;
    const maxPrice = document.getElementById('filter-max-price').value;

    const filters = {};
    if (category) filters.category = category;
    if (region) filters.region = region;
    if (minPrice) filters.min_price = minPrice;
    if (maxPrice) filters.max_price = maxPrice;

    fetchProducts(filters);
}

function addToCart(productId) {
    fetch('/api/cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken // Include the CSRF token here
        },
        body: JSON.stringify({
            product: productId,
            quantity: 1
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        console.log('Success:', data);
        fetchCart();
    })
    .catch(error => console.error('Error:', error));
}


function fetchCart() {
    fetch('/api/cart/')
        .then(response => response.json())
        .then(data => {
            const cartList = document.querySelector('#cart-list ul');
            cartList.innerHTML = '';
            data.forEach(item => {
                const li = document.createElement('li');
                li.className = 'list-group-item d-flex justify-content-between align-items-center';
                li.innerHTML = `
                    ${item.product_name} - ${item.quantity}
                    <span>
                        <h4>Quantity</h4>
                        <input type="number" class="form-control d-inline-block w-auto" value="${item.quantity}" onchange="updateCartItemQuantity(${item.id}, this.value)">
                        <button class="btn btn-danger btn-sm ml-2" onclick="removeFromCart(${item.id})">Remove</button>
                    </span>
                `;
                cartList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching cart:', error));
}


function updateCartItemQuantity(cartItemId, newQuantity) {
    fetch(`/api/cart/${cartItemId}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken

        },
        body: JSON.stringify({ quantity: newQuantity }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Cart item updated:', data);
        fetchCart();
    })
    .catch(error => console.error('Error updating cart item:', error));
}


function removeFromCart(itemId) {
    fetch(`/api/cart/${itemId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            console.log('Cart item deleted successfully');
            fetchCart();
        } else {
            console.error('Error deleting cart item:', response.statusText);
        }
    })
    .catch(error => console.error('Error:', error));
}



function toggleCart() {
    const cartList = document.getElementById('cart-list');
    if (cartList.style.display === 'none') {
        cartList.style.display = 'block';
    } else {
        cartList.style.display = 'none';
    }
}