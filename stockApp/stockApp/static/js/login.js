const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector('.invalid_feedback');
const emailField = document.querySelector("#emailField");
const emailfeedBackArea = document.querySelector('.emailFeedbackArea');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const submitBtn = document.querySelector('.submit-btn');


const oldpsw = document.getElementById('passwordField');


const handleToogleInput = (e)=>{
    if(oldpsw.getAttribute('type')==='password'){
        showPasswordToggle.classList.remove('fa-eye')
        showPasswordToggle.classList.add('fa-eye-slash')
        oldpsw.setAttribute("type","text");
    } else{
        oldpsw.setAttribute("type","password")
        showPasswordToggle.classList.remove('fa-eye-slash')
        showPasswordToggle.classList.add('fa-eye')
    }
}

showPasswordToggle.addEventListener('click',handleToogleInput);
