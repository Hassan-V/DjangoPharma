document.addEventListener('DOMContentLoaded', function () {
    // Function to handle removal from cart
    function handleRemoveFromCart(e) {
        e.preventDefault();
        const productId = e.currentTarget.dataset.productId;
        if (!productId) return; // Exit if productId is null
        removeFromCart(productId);
    }

    // Function to handle quantity update
    const handleQuantityChange = debounce(function(e) { // target id == 
        const productId = e.target.closest('form').querySelector('input[name="product-id"]').value;
        const quantity = e.target.value;
        updateCartQuantity(productId, quantity);
    }, 500);

    // Attach event listeners to Remove links
    document.querySelectorAll('a#prevent-default').forEach(item => {
        item.addEventListener('click', handleRemoveFromCart);
    });

    // Attach event listeners to quantity range inputs
    document.querySelectorAll('input[type="range"]').forEach(item => {
        item.addEventListener('input', handleQuantityChange); // or 'change' if you prefer to update on release
    });

    function removeFromCart(productId) {
        fetch('/remove_from_cart/' + productId + "/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Assuming Django CSRF token is needed
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'product_id': productId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Remove the cart item from the DOM or update the UI as needed
                window.location.reload();
                console.log('Item removed');
            }
        });
    }

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    function updateCartQuantity(productId, quantity) {
        // Immediately calculate and update the UI based on assumed pricing rules
        const assumedPrice = calculatePriceOnClientSide(productId, quantity);
        updateUIWithNewPrice(productId, assumedPrice);

        // Then, confirm the price with the server
        fetch('/update_cart_item_quantity/' + productId + "/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'quantity': quantity })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Update the UI with the server-confirmed price if different
                if (data.new_total_price !== assumedPrice) {
                    updateUIWithNewPrice(productId, data.new_total_price);
                }
                // Update the overall cart total
                updateCartTotal(data.cart_total);
            } else {
                // Handle error
            }
        })
        .catch(error => {
            // Handle fetch error
        });
    }

    function calculatePriceOnClientSide(productId, quantity) {
        const price = quantity * getProductUnitPrice(productId);
        return parseFloat(price.toFixed(2));
    }

    function getProductUnitPrice(productId) {
        const itemPriceElement = document.querySelector(`.price-per-unit[data-product-id="${productId}"]`);
        if (itemPriceElement) {
            return parseFloat(itemPriceElement.textContent.replace('$', ''));
        } else {
            console.error('Error: Item price element not found.');
            return null;
        }
    }

    function updateUIWithNewPrice(productId, newPrice) {
        const itemPriceElement = document.querySelector(`.total-item-price[data-product-id="${productId}"]`);
        if (itemPriceElement) {
            // Ensure the price is always formatted to two decimal places before updating the UI
            const formattedPrice = parseFloat(newPrice).toFixed(2);
            itemPriceElement.textContent = `$${formattedPrice}`;
        } else {
            console.error('Error: Item price element not found.');
        }
    }

    function updateCartTotal(cartTotal) {
        const cartTotalElement = document.querySelector('.cart-total');
        if (cartTotalElement) {
            cartTotalElement.textContent = `$${parseFloat(cartTotal).toFixed(2)}`;
        } else {
            console.error('Error: Cart total element not found.');
        }
    }

    // Function to get CSRF token for Django
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
