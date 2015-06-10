/*
Under MIT License. Please see accompanying LICENSE document.
*/

(function () {
    $(document).ready(function () {
        var loader = $('#loader');
        loader.addClass('hide');

        $('#converter').click(function (){
            var text = $('#eng').text().trim();
            if (text == '') return;
            var dest = $('#bng');

            loader.removeClass('hide');
            loader.addClass('show');

            $.ajax(
                ('/api/v1/' + text),
                {
                    success: function (d, status, req) {
                        dest.html(d);
                        loader.removeClass('show');
                        loader.addClass('hide');
                    },
                    error: function () {
                        loader.removeClass('show');
                        loader.addClass('hide');
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