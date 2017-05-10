/*

	This is a simple snippet for copy-paste purposes.

*/
$.ajax({
    url: 'test.html',
    cache: false,
    async: true,
    contentType: "application/json", // 'multipart/form-data', 'text/plain'
    dataType: "json", //(xml, json, script, or html)
    indexValue: i,
    type: 'GET', // 'POST', remember if POST is used and you're using an active session, you need to remove contentType and/or dataType
    data: { 
        'param_a': 1,
        'param_b': 'value_b',
        '_csrf_token': '{{ csrf_token() }}' // i.e. token to prevent CSRF 
    },
    success: function(data, status, jqXHR) { 
        console.log("response: ", data);
        console.log("you may want to send data into this callback as ", indexValue);
    },
    error: function(jqXHR, status, error) { 
        console.log("response: ", jqXHR);
        console.log("status: ", status);
        console.log("error: ", error);
    },
    complete: function(jqXHR, status) { 
        console.log("response: ", jqXHR);
        console.log("status: ", status);
    }
});



console.log('onesmartajax.js 0.0.1');

