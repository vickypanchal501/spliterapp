/*!
* Start Bootstrap - Personal v1.0.1 (https://startbootstrap.com/template-overviews/personal)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-personal/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
function verifyPassword() {
    let pass1 = document.getElementById("form3Example4c").value;
    let pass2 = document.getElementById("form3Example4cd").value;
      let match = true;
    if (pass1 != pass2) {
      //alert("Passwords Do not match");
      document.getElementById("form3Example4c").style.borderColor = "#ff0000";
      document.getElementById("form3Example4cd").style.borderColor = "#ff0000";
      match = false;
    }
    else {
      alert("Passwords match.");
    }
    return match;
  }
  



