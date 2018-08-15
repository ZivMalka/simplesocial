

$(document).ready(function() {


       $(function() {
            $('.date-picker1').datepicker( {
            changeMonth: true,
            changeYear: true,
            showButtonPanel: true,
            dateFormat: 'yy',
            onClose: function(dateText, inst) {
                $(this).datepicker('setDate', new Date(inst.selectedYear, 1, 1));
            }
            });
             $('.date-picker1').focus(function () {
	        	$(".ui-datepicker-calendar").hide();
	        	$(".ui-datepicker-month").hide();
			});
        });

    $( function() {
    $( ".datepicker" ).datepicker();
  } );

    $(".a").click(function () {
        var modal = document.getElementByClassName("modal");
        window.onclick = function (event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
    });

         $(function() {
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


    // Apply the search
 $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });


})


