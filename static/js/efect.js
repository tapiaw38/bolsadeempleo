ListService();
function ListService(){
  $.ajax({
  type:"get",
  url: "{% url 'list_json' %}",
  data: $(this).serialize(),
  dataType: "json",
  cache:false,
  success: function(response){
    console.log(response);
    var html;
    var url_facebook = "{% static 'img/facebook.png' %}";
    var sitio = "{% static 'img/sitio.png'%}";
    var estrella = "{% static 'img/estrella.png' %}";
    var eliminar = "{% static 'img/eliminar.png' %}";
     
    $.each(response, function(index,element){
      if (element.user == element.request_user) {
        var elim = '<a type="button" class="mb-3 float-right ml-3 eliminar" name="'+element.id+'"><img src="'+eliminar+'" alt="" width="30" height="30" class="color-expand"></a>';
      }else{
        elim = "";
      };
      if (element.facebook_url != null) {
        facebook = '<a href="'+element.facebook_url+'"  class="mb-3 float-right"><img src="'+url_facebook+'" alt="" width="30" height="30" class="color-expand"><a/>';
      }else{
        facebook = "";
      };
      if (element.direction != null) {
        directions = '<img src="'+sitio+'" alt="" width="20" height="20" class=" mr-2"><p class="mt-0 mb-1 text-secondary">'+element.direction+'</p></form>';
      }else{
        directions = '<img src="'+sitio+'" alt="" width="20" height="20" class="d-none mr-2"><p class="mt-0 mb-1 text-secondary"></p></form>';
      };
      
      html = '<div class="target pl-3 pr-3 pt-3 pb-2 mt-2 none'+element.id+'">',
      html += '<div class="media">';
      html +='<a href="/user/'+element.user+'">',
      html +='<img class="mr-3 rounded-circle" src="'+element.picture+'" alt="'+element.user+'" width="50" height="50"></a>',
      html +='<div class="media-body">',
      html +='<h5 class="mt-0">@'+element.user+'</h5>',
      html +='<h6 class="ml-0 mt-1">'+element.title+'</h6></div>',
      html += facebook,
      html +='</div>',
      html +='<a href="" data-toggle="modal" data-target="#'+element.user+'">',
      html +='<img class="img-fluid mt-3 border rounded" src="'+element.picture_logo+'" alt="'+element.title+'"><span class="badge badge-primary">'+element.category+'</span></a>',
      html +='<p class="mt-1 mb-0 text-primary">'+element.description+'</p>',
      html +=' <form class="form-inline">',
      html +=directions,
      html +='<span class="badge ml-0 mt-0">'+element.created+'</span>',
      html +='<div class="mt-0 mb-3">',
      html +='<hr>',
      html +='<a id="like" type="button" class="like" name="'+element.id+'"><img src="'+estrella+'" alt="" width="30" height="30"class="color-expand mb-1 mr-2"></a>',
      html +='<span class="badge badge-pill mb-2 p-2 text-light d-inline mt-0" style="background-color: rgb(255, 192, 31);"><strong id="service'+element.id+'">'+element.liked+'</strong> Estrellas</span>',
      html += elim,
      html +='',
      html +='',
      html +='</div>',
      html +='</div>',
      html +='</div>';
      
                
      $("#list_json").append(html);
    })//end each
     
     
  }//end success
  });//end ajax
};
         
           //list ajax
     
           //liked
           $('body').on('click', '.like',function(event){
             event.preventDefault();
             $.ajax({
             type: "POST",
             url: "{% url 'like' %}",
             data: {'service_id': $(this).attr('name'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
             dataType: "json",
             cache:false,
             success: function(response) {
                //alert(' likes count is now ' + response.likes_count);
                var count = "";
                count+= response.likes_count;
                var id = response.service_pk;
                
     
                $("#service"+id).html(count);
     
             },
             error: function(rs, e) {
                 alert(rs.responseText+ "error");
               },
             });
     
           });
           //delete
           $('body').on('click','.eliminar',function(event){
             event.preventDefault();
             $(".load").show();
             if(confirm("¿Estás seguro de eliminar esté servicio?")){
               $.ajax({
                 type: "POST",
                 url: "{% url 'delete' %}",
                 data: {'service_id': $(this).attr('name'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
                 dataType: "json",
                 beforeSend:function(){
     
                   
                 },
                 success: function(response) {
                   $(".load").show();
                   var id = response.service_pk;
                   $(".none"+id).addClass("graysacale");
                   $(".none"+id).hide(1000);
                 }//end success
     
               }).always(function(){
                
               })
             }//endif
             else{
               return false;
             };
             //$("#list_json").text("");
             //ListService();
           });
     
     
     
     
     
     
     
           /*
             //liked ajax
         $('.like').click(function(){
         console.log("dentro de funcion like");
         $.ajax({
            type: "POST",
            url: "{% url 'like' %}",
            data: {'service_id': $(this).attr('name'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
            dataType: "json",
            success: function(response) {
                //alert(' likes count is now ' + response.likes_count);
                var count = "";
                count+= response.likes_count;
                var id = response.service_pk;
                
     
                $("#service"+id).html(count);
     
            },
             error: function(rs, e) {
                 alert(rs.responseText+ "error");
               },
             });
           })
       //delete service ajax
      $('.eliminar').click(function(){
       if(confirm("¿Estás seguro de eliminar esté servicio?")){
             $.ajax({
               type: "POST",
               url: "{% url 'delete' %}",
               data: {'service_id': $(this).attr('name'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
               dataType: "json",
               beforeSend:function(){
                 $(".load").show();
                 
                 
               },
               success: function(response) {
                   var id = response.service_pk;
                   $("#none"+id).addClass("graysacale")
                   $("#none"+id).hide(1000);
     
               },
               error: function(rs, e) {
                     alert(rs.responseText+ "error");
               },
             })//endajax
             .always(function() {
               $(".load").hide();
             });
         }//endif
       else{
         return false;
         }
     });
     
     */