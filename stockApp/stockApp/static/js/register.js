const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector('.invalid_feedback');
const emailField = document.querySelector("#emailField");
const emailfeedBackArea = document.querySelector('.emailFeedbackArea');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const submitBtn = document.querySelector('.submit-btn');


const oldpsw = document.getElementById('passwordField');
const psw_conf = document.getElementById('passwordField2');


const handleToogleInput = (e)=>{
    if(oldpsw.getAttribute('type')==='password'){
        showPasswordToggle.classList.remove('fa-eye')
        showPasswordToggle.classList.add('fa-eye-slash')
        oldpsw.setAttribute("type","text");
        psw_conf.setAttribute("type", "text")
    } else{
        oldpsw.setAttribute("type","password")
        psw_conf.setAttribute("type","password")
        showPasswordToggle.classList.remove('fa-eye-slash')
        showPasswordToggle.classList.add('fa-eye')
    }
}

showPasswordToggle.addEventListener('click',handleToogleInput);



emailField.addEventListener('keyup',(e)=>{
    const emailVal = e.target.value;

    emailField.classList.remove('is-invalid')
    emailfeedBackArea.style.display = "none";

        if(emailVal.length > 0){
            fetch("/authentication/validate-email",{
                body: JSON.stringify({email: emailVal}),
                method: "POST",
            })
                .then(res=>res.json())
                .then((data)=>{
                    console.log(data);
                    if(data.email_error){
                        emailField.classList.add('is-invalid')
                        emailfeedBackArea.style.display = "block"
                        emailfeedBackArea.innerHTML='<p>'+ data.email_error +'</p>'
                        submitBtn.setAttribute("disabled","disabled");
                        submitBtn.disabled = true;
                    } else {
                        submitBtn.removeAttribute("disabled");
                    }
                });
        }
})

usernameField.addEventListener('keyup',(e)=>{
    const usernameVal = e.target.value;


usernameField.classList.remove('is-invalid')
feedBackArea.style.display = "none";

    if(usernameVal.length>0){
        fetch("/authentication/validate-username",{
            body: JSON.stringify({username: usernameVal}),
            method: "POST",
        })
            .then(res=>res.json())
            .then((data)=>{
                console.log(data);
                if(data.username_error){
                    usernameField.classList.add('is-invalid')
                    feedBackArea.style.display = "block"
                    feedBackArea.innerHTML='<p>'+ data.username_error +'</p>'
                    submitBtn.setAttribute("disabled","disabled");
                    submitBtn.disabled = true;
                } else {
                    submitBtn.removeAttribute("disabled");
                }
            });
    }
});

var plan = localStorage.getItem('plan_id')

window.onload = function(){
    premium = document.getElementById(plan)
    premium.selected = true;
}



