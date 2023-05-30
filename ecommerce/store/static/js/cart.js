let updateBtn = document.getElementsByClassName('add-to-cart')

for(let i=0; i<updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        let itemId = this.dataset.item //from button in html and action
        let action = this.dataset.action
        console.log("itemId: ", itemId, "action: ", action)

        console.log('USER: ', user)
        if (user === 'AnonymousUser'){
            console.log('User is not logged in')
        }else{
            addUserOrder(itemId, action)
        }
    })
}

function addUserOrder(itemId, action) {
    console.log('User is logged in, sending data...')
    console.log("itemId:", itemId)
    let url = '/add_to_cart/'
    console.log('Data:', JSON.stringify({'itemId': itemId, 'action': action}));

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'itemId': itemId, 'action': action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data:', data)
    })
}