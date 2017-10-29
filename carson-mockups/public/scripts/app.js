'use strict';

var journalEntry = {};

$(document).ready(function(){
  if (localStorage.journals) {
    var template = Handlebars.compile($('#template').html());
    var entries = JSON.parse(localStorage.journals);
    entries.map(function(entry){
      $('.container-transparent').append(template(entry));
    });
  }
});

$('#details').on('click', function(){
  console.log('above compiler');
  var template = Handlebars.compile($('#template-entry').html());
  console.log('above entries var');
  var entries = JSON.parse(localStorage.journals);
  console.log('above map');
  entries.map(function(entry){
    $('#detailed-entries').append(template(entry));
  });
  document.location.href = 'https://carson-learning-journal.herokuapp.com/detailed_entry.html';
});

$(document).scroll(function() {
  var navbar = $('nav');
  var dataHomeEl = $('.data-home');
  if ($(window).scrollTop() >= 152) {
    dataHomeEl.css('padding-top', '7.8%');
    navbar.addClass('sticky');
  } else {
    dataHomeEl.css('padding-top', '0%');
    navbar.removeClass('sticky');
  }
});

$('#payment-send').on('click', function(e) {
  e.preventDefault();
  if($('#user-form-invoice').val().length > 0 && $('#user-form-bill').val().length > 0 && document.getElementById('user-checkbox').checked) {
    var serviceCharge = $('#user-form-bill').val() * 100;
    var amount = serviceCharge + Math.round(serviceCharge * 0.032);
    handler.open({
      name: 'TRON Communication',
      description: 'Pay your Service Charge bill here!',
      amount: amount,
      allowRememberMe: false,
      zipCode: true,
      image: 'https://upload.wikimedia.org/wikipedia/commons/d/d5/Phone_Shiny_Icon.svg',
      token: function(token) {
        token.amount = amount;
        $.post('/charge', token)
        .then(function(result){
          console.log(result);
          $('#payment-form').html('<h4 id="success-header" class="form-header">Payment Successful<span class="icon-checkmark"></span></h4><p class="section-text-medium">A receipt for this payment has been sent to the email address you provided.</p>');
        })
        .catch(function(err){
          console.log(err);
          $('#payment-form').html('<h4 id="declined-header" class="form-header">Payment Declined<span class="icon-cross"></span></h4><p class="section-text-medium">Something went wrong and your payment was not accepted. Please click the Home button, refresh the page, and try again. If following these steps does not resolve the issue, please contact us using the form provided on this website.</p>');
        });
      }
    });
  } else {
    alert('You must fill in the Invoice Number and Service Charge fields, as well as check the box, in order to proceed.');
  }
});

$('#entry-button').on('click', function(){
  var journalDate = $('#journal-date').val();
  var journalName = $('#journal-name').val();
  var journalContent = $('#journal-content').val();
  if(journalDate.length > 0 && journalName.length > 0 && journalContent.length > 0) {
    if (localStorage.journals) {
      var journalList = JSON.parse(localStorage.journals);
      journalEntry.title = journalName;
      journalEntry.date = journalDate;
      journalEntry.entry = journalContent;
      journalList.push(journalEntry);
      localStorage.journals = JSON.stringify(journalList);
    } else {
      var journalList = [];
      journalEntry.title = journalName;
      journalEntry.date = journalDate;
      journalEntry.entry = journalContent;
      journalList.push(journalEntry);
      localStorage.journals = JSON.stringify(journalList);
    }
  } else {
    alert('You must fill in the Date, Title, and Entry fields bro.');
  }
});
