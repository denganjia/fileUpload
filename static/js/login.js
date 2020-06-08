// function f() {
//     const input_user = document.getElementById("account");
//     input_user.setAttribute("placeholder", "username");
//
//
//     const input_password = document.getElementById("password");
//     input_password.setAttribute("placeholder","password");
//
// }
$(document).ready(function () {
    $("#account").attr("placeholder", "username");
    $("#password").attr("placeholder", "password");
    // $("#submit").click(function () {
    //     $("#result").text("用户名或密码错误！请重新输入")
    // })
})
