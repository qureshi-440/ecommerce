var updatebtn = document.getElementsByClassName('update-cart');

for (var i =0; i < updatebtn.length;i++ ){
    updatebtn[i].addEventListener('click',function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log("product-id :", productId ,'action :',action)

        console.log('user : ' , user)
        if (user === 'AnonymousUser') {
            getCookieitem(productId,action)
        }else{
            updatecartloggedin(productId,action)
        }
    })
}


function getCookieitem(productId,action) {
    console.log('User not authenticated');

    if (action === 'add') {
        if (cart[productId] == undefined)  {
            cart[productId] = {'quantity':1}
        }else {
            cart[productId]['quantity'] += 1;
        }
    } 
    if (action === 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId]
        }
    }
    console.log('cart = ',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}


function updatecartloggedin(productId,action) {
    console.log('user is logged in ,sending data ...,')

    var url = '/update-cart/'

    fetch(url,{
        method :'POST',
        headers : {
            'Content-Type':'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body : JSON.stringify({'productid':productId,'action':action}),
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data :',data)
        location.reload()
    })
}

$('.to-form').change(function () {
    if (this.getAttribute('value') === this.value) {
        // setting the original 'lastvalue' data property
        $(this).data('lastvalue', this.value);
    } else {
        // take whatever action you require here:
        console.log(this.value < $(this).data('lastvalue') ? 'decrement' : 'increment');
        if (this.value < $(this).data('lastvalue')) {
            var action = 'remove';
            var productId = this.dataset.product;
            console.log("decrement");
            if (user === 'AnonymousUser') {
                getCookieitem(productId,action)
            }else{
                updatecartloggedin(productId,action);
            }
            
        } else {
            var action = 'add';
            var productId = this.dataset.product;
            console.log("increment");
            if (user === 'AnonymousUser') {
                getCookieitem(productId,action)
            }else{
                updatecartloggedin(productId,action);
            }
        }
        // update the lastvalue data property here:
        $(this).data('lastvalue', this.value);
    }
}).change();

