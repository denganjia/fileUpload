// function input() {
//     const old_password= document.getElementById("old_password");
//     old_password.setAttribute("placeholder","旧密码");
//     const new_password= document.getElementById("new_password");
//     new_password.setAttribute("placeholder","新密码");
//     const new_password_repeat= document.getElementById("new_password_repeat");
//     new_password_repeat.setAttribute("placeholder","重复新密码");
// }
$(document).ready(function () {
    $("#old_password").attr("placeholder","旧密码");
    $("#new_password").attr("placeholder","新密码");
    $("#new_password_repeat").attr("placeholder","重复新密码");
})