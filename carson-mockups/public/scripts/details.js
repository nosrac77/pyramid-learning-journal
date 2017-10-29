'use strict';

$(document).ready(function(){
  if (localStorage.journals) {
    var template = Handlebars.compile($('#template-entry').html());
    var entries = JSON.parse(localStorage.journals);
    entries.map(function(entry){
      $('.container-transparent').append(template(entry));
    });
  }
});
