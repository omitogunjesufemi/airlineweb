
function changePrice(flight_class){
    let price = document.getElementById('price').value
    let flight_price;
    if (flight_class === 'First') {
        flight_price = 2 * parseFloat(price);
        document.getElementById('price').value = flight_price;
    }
    else if(flight_class === 'Business'){
        flight_price = 1.5 * parseFloat(price);
        document.getElementById('price').value = flight_price;
    }
    else if(flight_class === 'Economic'){
        flight_price = parseFloat(price);
        document.getElementById('price').value = flight_price;
    }

}

function main(){
document.getElementById('first').addEventListener("click", () => changePrice('First'));
document.getElementById('business').addEventListener("click", () => changePrice('Business'));
document.getElementById('economic').addEventListener("click", () => changePrice('Economic'));
}

main();