

$(document).ready(function(){

       $(".a").click(function(){
var modal = document.getElementByClassName("modal");
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}}
   {
            $('.date-picker').datepicker( {
            changeMonth: true,
            changeYear: true,
            showButtonPanel: true,
            onClose: function(dateText, inst) {
                $(this).datepicker('setDate', new Date(inst.selectedYear, inst.selectedMonth, 1));
            }
            });
             $('.date-picker').focus(function () {
	        	$(".ui-datepicker-calendar").hide();
			});
        });




}