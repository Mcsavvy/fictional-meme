shop = {
    updateCart: function(number) {
        if (isNone(number)) {
            cart = `<icon class="fas fa-shopping-cart stroke-r-bg-1"></icon>`
        } else {
            cart = `<icon class="fas fa-shopping-cart r-bg"></icon>
                <span class="badge rounded-pill badge-notification r-bg bg-pm" id="cart-count">
                  <i id="cart-counter">${number}</i>
                </span>`
        }
        $('#shopping-cart').html(cart)
    },
    updateWishlist: function(number) {
        if (isNone(number)) {
            wish = '<icon class="fas fa-heartbeat stroke-r-bg-1"></icon>'
        } else {
            wish = `<icon class="fas fa-heartbeat r-bg"></icon>
            <span class="badge rounded-pill badge-notification r-bg bg-pm" id="wish-count">
              <i id="wish-counter">${number}</i>
            </span>`
        }
        $('#wishlist').html(wish)
    },
    updateNotification: function(number){
        if (isNone(number)) {
            notification = `<icon class="fas fa-bell stroke-r-bg-1"></icon>`
        } else {
            notification = `<icon class="fas fa-bell r-bg ring"></icon>
            <span class="badge rounded-pill badge-notification r-bg bg-pm" id="notification-count">
              <i id="notification-counter">
                ${number}
              </i>
            </span>`
        }
        $('#notification').html(notification)
    }
}
