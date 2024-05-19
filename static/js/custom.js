$(document).ready(function () {
    // Increment quantity
    $('.increment-btn').click(function (e) {
        e.preventDefault();
        var $input = $(this).closest('.input-group').find('input[name="quantity-input"]');
        var value = parseInt($input.val(), 10);
        value = isNaN(value) ? 0 : value;
        if (value < 10) {
            $input.val(value + 1);
        }
    });

    // Decrement quantity
    $('.decrement-btn').click(function (e) {
        e.preventDefault();
        var $input = $(this).closest('.input-group').find('input[name="quantity-input"]');
        var value = parseInt($input.val(), 10);
        value = isNaN(value) ? 0 : value;
        if (value > 1) {
            $input.val(value - 1);
        }
    });

    $('.addToCartBtn').click(function () {
        // Retrieve product ID and quantity
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            type: 'POST',
            url: "/add-to-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", token);
            },
            success: function (response) {
                console.log(response);
                alertify.success(response.status);
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText); // Log the error message
                alertify.error("An error occurred while adding the product to the cart.");
            }
        });
    });

    // update cart
    $('.changeQuantity').click(function () {
        // Retrieve product ID and quantity
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            type: 'POST',
            url: "/update-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },

            success: function (response) {
            },

        });
    });
    // delete cart item
    $('.delete-cart-item').click(function () {
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: 'POST',
            url: "/delete-cart-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },

            success: function (response) {
                alertify.success(response.status);
                $('.cartdata').load(location.href + " .cartdata");
            },

        });

    });




});
