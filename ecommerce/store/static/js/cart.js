let updateBtn = document.getElementsByClassName('add-to-cart')

for(let i=0; i<updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        let itemId = this.dataset.item //from button in html and action
        let action = this.dataset.action
        if(document.querySelector('input[name="size"]')== null){
            addUserOrder(itemId, 5, action);
            return;
        }
        let element = document.querySelector('input[name="size"]:checked');
        let size_id = element.value;
        if (user === 'AnonymousUser'){
            console.log('User is not logged in')
            // redirekcija na login stranu
            //window.location.replace("http://http://127.0.0.1:8000/login/")
        }else{
            addUserOrder(itemId, size_id, action)
        }
    })
}



function addUserOrder(itemId, size_id, action) {
    console.log('User is logged in, sending data...')
    console.log("itemId:", itemId)
    let url = '/add_to_cart/'
    console.log('Data:', JSON.stringify({'itemId': itemId, 'size':size_id, 'action': action}));

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'itemId': itemId, 'size_id': size_id, 'action': action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) => {
        console.log('Data received:', data);
        if (data.success) {
            console.log('Success message received:', data.success);
            updateNumberOfProductsInCart();
        } else {
            console.log('No success message received');
        }
    })
    .catch((error) => {
        console.error('Error occurred:', error);
    });
}


function changeImage(thumbnail) {
    var mainImage = thumbnail.closest('.images').querySelector('.card-img-top');
    mainImage.src = thumbnail.src;
}