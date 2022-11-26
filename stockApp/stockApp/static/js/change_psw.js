const oldpsw = document.getElementById('oldpsw');
const newpsw = document.getElementById('psw');
const psw_conf = document.getElementById('pswc');
const showPasswordToggle = document.querySelector('.showPasswordToggle');

console.log("it works")

const handleToogleInput = (e)=>{
    if(oldpsw.getAttribute('type')==='password'){
        showPasswordToggle.classList.remove('fa-eye')
        showPasswordToggle.classList.add('fa-eye-slash')
        oldpsw.setAttribute("type","text");
        newpsw.setAttribute("type", "text")
        psw_conf.setAttribute("type", "text")
    } else{
        oldpsw.setAttribute("type","password")
        newpsw.setAttribute("type","password")
        psw_conf.setAttribute("type","password")
        showPasswordToggle.classList.remove('fa-eye-slash')
        showPasswordToggle.classList.add('fa-eye')
    }
}

showPasswordToggle.addEventListener('click',handleToogleInput);