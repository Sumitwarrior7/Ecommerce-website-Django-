function updateUserOrder(productID, action){
  console.log("User is authenticated");

  var url = 'update_item/'
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({"productId": productID, "action": action})
  })
  .then((response)=>{
    return response.json();
  })
  .then((data)=>{
    console.log('data :', data);
    location.reload();
  })
}


//For adding cookie to web server :-
function addCookieItem(productId, action) {
    console.log("user not logged in ......")
    console.log(productId)
    console.log(action)

    if(action=='add'){
        console.log('add-if')
        if(cart[productId] == null){
            console.log("New product is created in cart ...")
            cart[productId] = {'quantity':1};
        }else{
            cart[productId]['quantity'] += 1;
        }
    }

    if(action=='remove'){
        console.log('remove-if')
        cart[productId]['quantity'] -= 1;

        if(cart[productId]['quantity'] <= 0){
            console.log('Remove item ...');
            delete cart[productId]
        }
    }

    console.log('cart neeche likha hai :-')
    console.log(cart)

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}



$(".btn-update").click(function(){
  var productId = $(this).attr('data-product');
  var action = $(this).attr('data-action');

  if(user=='AnonymousUser'){
    addCookieItem(productId, action);
  }else{
    updateUserOrder(productId, action);
  }
})



