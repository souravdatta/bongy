/*
Under MIT License. Please see accompanying LICENSE document.
*/

(function () {
    $(document).ready(function () {
        $('#converter').click(function (){
            var text = $('#eng').val();
            var dest = $('#bng');
            $.ajax(
                ('/api/v1/' + text),
                {
                    success: function (d, status, req) {
                        dest.html(d);
                    },
                    error: function () {
                        console.log('Error retrieving result from server...')
                    }
                }
            );
        });

        $('#mapping').click(function () {
            window.open('/mappings');
        });
    });
})();