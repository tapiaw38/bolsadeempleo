$('.like').click(function(){
    $.ajax({
       type: "POST",
       url: "{% url 'like' %}",
       data: {'service_id': $(this).attr('name'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
       dataType: "json",
       success: function(response) {
           alert(' likes count is now ' + response.likes_count);
           var count = "";
           count+= response.likes_count;
       },
       error: function(rs, e) {
            alert(rs.responseText+ "error");
       },
    });
 })