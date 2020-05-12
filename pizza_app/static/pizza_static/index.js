document.addEventListener('DOMContentLoaded', () => { 
    
    if(document.getElementById('alert').innerHTML != "" ){        
        alert(document.getElementById('alert').innerHTML);
        document.querySelector('#alert').innerHTML = ""; 
        window.location = '/';
    }

    document.querySelector('#sign_up_form').onsubmit = () => { 
        if (document.querySelector('#sign_pswd').value != document.querySelector('#sign_rpswd').value){
            alert(`Password and Repearted Password don't match`);
            return false;
        }
   
    }; 

}); 