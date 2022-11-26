const symbolselect = document.getElementById('slst1')
const priceBtn = document.getElementById('crpbtn')
const priceField = document.getElementById('stprc')


window.onload = function(){
  fetch("check-api").then((res) => res.json()).then((results)=>{
    console.log(results)
    var requests = results.remainingRequests
    if (requests<=0){
      priceBtn.style.display = 'none'
    }
  })
}

window.onload = function(){
  fetch('https://api.exchangerate.host/latest?base=USD').then((res) => res.json()).then((results)=>{
    var currency = 'EUR'
    console.log(results.rates[currency])
  })
}



priceBtn.onclick = function(){
  var symbol = symbolselect.value
  var url = "https://financialmodelingprep.com/api/v3/profile/"+ symbol +"?apikey="
  fetch(url)
    .then((res) => res.json())
      .then((results) => {
        var cur_price = results[0].price
        fetch("user-preference").then((res) => res.json()).then((results)=>{
          console.log(results)
          var currency = results.preferences
          fetch('https://api.exchangerate.host/latest?base=USD').then((res) => res.json()).then((results)=>{
            var rate = results.rates[currency]
            var current_price = cur_price.toFixed(2) * rate 
            priceField.value = current_price.toFixed(2)
            console.log(currency)
            fetch('increase-api').then((res) => res.json()).then((results)=>{
              console.log(results)
            })
          })
        })
    })
  }




















