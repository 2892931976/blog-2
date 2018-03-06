function changePassword() {
    $('#changePasswordFormModal').modal();
}

function changecategory() {
    $('#changeCategoryFormModal').modal();
}

function createcategory() {
    $('#createCategoryFormModal').modal();
}

function createmenu() {
    $('#createMenuFormModal').modal();
}

function checkChangePasswordForm() {
    var password = $('#password').val();
    var password2 = $('#password2').val();
    if (password != password2) {
        $('#group_password2').addClass('has-error');
        $('#password2_err').show();
        return false;
    } else {
        $('#changePasswordForm').submit();
        return true;
    }
}

function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]
}

$("#keyword_form").submit(function(){
    event.preventDefault(); //不写的话， 会提交两次 
    keyword = $("#keyword").val() 
    window.location.href="/?keyword=" + keyword
    
   // var keyword = $("#keyword").val() ;
   // var newHref = xtparam.setParam(window.location.href,'keyword',keyword);
   // window.location = newHref;
});