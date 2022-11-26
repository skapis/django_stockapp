const free = document.getElementById('1')
const investor = document.getElementById('2')
const trader = document.getElementById('3')


free.onclick = function(){
    var id = free.id
    localStorage.setItem("plan_id", id)
}

investor.onclick = function(){
    var id = investor.id
    localStorage.setItem("plan_id", id)
}

trader.onclick = function(){
    var id = trader.id
    localStorage.setItem("plan_id", id)
}