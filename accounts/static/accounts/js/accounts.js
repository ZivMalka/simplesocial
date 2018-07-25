

$(document).ready(function() {

    function myFunction() {
        var modal = document.getElementByClassName("modal");
        window.onclick = function (event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }


    }
}