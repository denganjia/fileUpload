function f() {
    const input_user = document.getElementById("account");
    input_user.setAttribute("placeholder", "username");

    // input_user.onselect = function () {
    //     input_user.setAttribute("value", "");
    // }
    // input_user.onfocus = function () {
    //     input_user.setAttribute("value", "");
    // }
    // input_user.onblur = function () {
    //     input_user.setAttribute("value", "username");
    // }

    const input_password = document.getElementById("password");
    // input_password.setAttribute("type","text");
    input_password.setAttribute("placeholder","password");
    // input_password.onfocus = function () {
    //     input_password.setAttribute("type","password");
    //     input_password.setAttribute("value","");
    // }
    // input_password.onselect = function () {
    //     input_password.onfocus(undefined);
    // }
    // input_password.onblur = function () {
    //     input_password.setAttribute("type","text");
    //     input_password.setAttribute("value","password");
    // }
}


