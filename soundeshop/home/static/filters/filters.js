let elementsArray = document.querySelectorAll("input[type=checkbox]");

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// var checkbox = document.querySelector("input[name=checkbox]");

// checkbox.addEventListener('change', function() {
//   if (this.checked) {
//     console.log("Checkbox is checked..");
//   } else {
//     console.log("Checkbox is not checked..");
//   }
// });



elementsArray.forEach(function(elem) {
    elem.addEventListener("change", function(e) {
        // This function does stuff
        var checkedBoxes = document.querySelectorAll('input[type=checkbox]:checked');
        var form = document.createElement("form");
  
        url =  '/catalogue/filtered_view/?'
        
        checkedBoxes.forEach(function(addelem){
            console.log(addelem);
            url += addelem.name +'='+addelem.value+'&'
        })
        // document.body.appendChild(form);
        console.log(url);
        // form.preventDefault;
        // console.log(checkedBoxes)
        // console.log(elem.value);
        // var cookie = getCookie('csrftoken').toString()
        // fetch('/catalogue/filtered_view/?' + new URLSearchParams({
        // category: elem.value,}))
        fetch(url)
        .then((response) => response.json())
        .then((json) => {
            var row_products = document.querySelectorAll(".row");
            row_products[3].innerHTML = json.inner_HTML;
            // console.log(row_products[3]);
            // console.log(json)
        });

        // fetch("/catalogue/filtered_view/"+ new URLSearchParams({
        //     foo: 'value',
        //     bar: 2,
        // })
        // , {
            
        //     method: 'POST',
        //     credentials: 'same-origin',
        //     headers: {
        //         Accept: 'application/json',
        //         'X-Requested-With': 'XMLHttpRequest', // Necessary to work with request.is_ajax()
        //         'X-CSRFToken': cookie,
        //         "Content-type": "application/json; charset=UTF-8"

        //       },
        //     mode: 'same-origin',            
        //     body: JSON.stringify({ "filter": elem.value }),
        //     })
        //     .then((response) => response.json())
        //     .then((json) => {
        //         var row_products = document.querySelectorAll(".row");
        //         row_products[3].innerHTML = json.panagia;
        //         // console.log(row_products[3]);
        //         // console.log(json)
        //     }
            // );

    });
});

btn = document.getElementById('filter_button')
btn.addEventListener("click", function(e){
    url =  '/catalogue/filtered_view/?'
        
    checkedBoxes.forEach(function(addelem){
        console.log(addelem);
        url += addelem.name +'='+addelem.value+'&'
    })
    // When button pressed also add the inputs of the price
});
