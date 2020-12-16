(document).ready(function () {

    let capacity = /[0-9]/;
    $.validator.addMethod("validNumber", function (value, element) {
        return this.optional(element) || capacity.test(value);
    });

    $("#aircraftForm").validate({
        rules: {
            aircraft_name: {required: true},
            aircraft_type: {required: true},
            capacity: {
                required: true,
                validNumber: true
            },
        },

        messages: {
            aircraft_name: {required: "Aircraft name cannot be empty"},
            aircraft_type: {required: "Please provide aircraft type"},
            capacity: {
                required: "Aircraft capacity is required",
                validNumber: "Numbers only are allowed!"
            }
        },

        errorElement: "span",
        errorClass: "help-block",

        submitHandler: function (aircraftForm){
            aircraftForm.submit();
        }
    });

    function submitForm() {

        $.ajax({
            url: 'register_aircraft',
            cache: false,
            type: 'POST',
            data: $('#aircraftForm').serialize(),
            dataType: JSON
        }).done(function (data) {

                $('.button').val('Creating aircraft...').prop('disabled', true);
                $('input[type=text]').prop('disabled', true);

                setTimeout(function () {

                    if (data.context['saved'] === 'success') {

                        $('#notify').slideDown('fast', function () {
                            $('#notify').html('<div class="alert alert-success">' + "Aircraft saved!" + '</div>');
                            $("#aircraftForm").trigger('reset');
                            $('input[type=text]').prop('disabled', false);
                            $('.button').val('Submit').prop('disabled', false);
                        }).delay(7000).slideUp('fast');


                    } else {

                        $('#notify').slideDown('fast', function () {
                            $('#notify').html('<div class="alert alert-danger">' + "An error occured!" + '</div>');
                            $("#aircraftForm").trigger('reset');
                            $('input[type=text]').prop('disabled', false);
                            $('.button').val('Submit').prop('disabled', false);
                        }).delay(7000).slideUp('fast');
                    }

                }, 7000);

            })
            // .fail(function () {
            //     $("#aircraftForm").trigger('reset');
            //     alert('An unknown error occured, Please try again Later...');
            // });
    }
});