$(document).ready(function()
{
    $('.delete_demo').bootstrap_confirm_delete(
        {
            heading: 'Delete',
            message: 'Are you sure you want to delete this?',
            data_type: null,

            callback: null,
            delete_callback:null,
            cancel_callback:null,


        });
});