
let price = document.getElementById('price');
let the_price = price.value;
console.log(the_price);

$( "#flight_class" ).change(function() {
        let flight_class = this.value;
        console.log(flight_class);

    if (flight_class === 'First') {
        $('#price').val((the_price * 2));
    }

    else if (flight_class === 'Business') {
        $('#price').val((the_price * 1.5));
    }
    else {
        $('#price').val(the_price)
    }
    });