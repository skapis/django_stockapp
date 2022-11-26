const emailField = document.querySelector("#emailField");
const emailfeedBackArea = document.querySelector('.emailFeedbackArea');


emailField.addEventListener('keyup',(e)=>{
    const emailVal = e.target.value;

    emailField.classList.remove('is-invalid')
    emailfeedBackArea.style.display = "none";

        if(emailVal.length > 0){
            fetch("/validate-email",{
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

