// AJAX VIEWS
function go_to(url) {
  $.ajax({
    type: 'GET',
    url: url,
    //data: attrs
    beforeSend: function () {
      //page_transition('hide');
      $('.contents').hide('slow');
    },
    success: function (data) {
      //page_transition('show')
      $('.contents').show('slow');
      $('.contents').html(data);
      
    }
  });
}

function put_to(url, data) {
  $.ajax({
      type: 'GET',
      url: url,
      data: data,
      beforeSend: function () {
        alert_sending();
      },
      success: function (data) {
        alert_success('Email has been sent');
      }
  });
}

//API DATA ROUTER
function get_data(route) {
  if (route == 'none') {
    return null;
  }
}

// CLICK MAPPINGS
$('.go_to').live('click', function() {
  var url = $(this).attr('href');
  go_to(url);
  return false;
});

$('.put_to').live('click', function() {
  var data_route = $(this).data('funct');
  var data = get_data(data_route);
  var url = $(this).attr('href');
  put_to(url, data);
  return false;
});

$('.search_in').live('click', function() {
  var target = '#' + $(this).data('target');
  var query = $(target).val();
  var options = parseInt($(this).data('options'));
  var i = 1;
  while (i <= options) {
    target = '#target_' + i;
    if ($(target).is(':checked') ){
      iframe_search(query, $(target).val());
    }
    i++;
  }
  return false
});
$('.search-input').live('keypress', function(e) {
  if(e.which == 13){
    $('.search_in').click();
  }
});

$('#calendar_show').live('click', function(e) {
  if ($('.calendar-container').hasClass('hidden')) {
    $('.calendar-container').show('slow');
    $('.calendar-container').removeClass('hidden');
    $('#calendar_toggle').removeClass('icon-chevron-down');
    $('#calendar_toggle').addClass('icon-chevron-up');
  }
  else {
    $('.calendar-container').hide('slow');
    $('.calendar-container').addClass('hidden')
    $('#calendar_toggle').addClass('icon-chevron-down');
    $('#calendar_toggle').removeClass('icon-chevron-up');
  }
  return false
});

// ALERT MESSAGES
function alert_success(msg) {
  $('.banner').html(
    '<div class="alert alert-success"><button type="button" class="close close_banner">×</button><strong>Success!</strong>' + msg + '</div>'
  );
}

function alert_sending() {
  $('.banner').html(
    '<div class="alert alert-info"><button type="button" class="close close_banner">×</button><strong>Sending!</strong> Wait a moment while i gather the data</div>'
  );
}

$('.close_banner').live('click', function() {
  $(this).parent().hide();
  return false;
});

//ANIMATION
function page_transition(dir) {
  if (dir == 'hide') {
    $('.contents').animate({ height: "0%", opacity:0.25 }, 500 );
  } 
  else {
    $('.contents').animate({ height: "100%", opacity:1 }, 500 );
  }
}

//IFRAME SEARCH
function iframe_search(query, target) {
  var url = '/search?search_query='+ query +'&search_target='+ target
  window.open(url);
}

// METHODS FOR CREATING A NEW EVENT

$('#create-event').live('click', function() {
  var form = '#calendar_form ';
  var artist = $(form + '#artist_input').val();
  var city = $(form + '#city_input').val();
  var state = $(form + '#state_input').val();
  var date = $(form + '#date_input').val();
  var hour = $(form + '#hr_input').val();
  var period = $(form + '#period_input').val();
  var sale_type = $(form + '#sale_type_input').val();
  var location = city + ', ' + state;
  var date_time = parse_time(date, hour, period);
  data = { date: date_time, artist: artist, location: location, sale_type: sale_type}
  $.ajax({
    type: 'POST',
    url: '/calendar',
    data: data,
    success: function (data) {
      alert_success(' Event successfuly created!');
      auth_link = '<a href="' + data +'" target="_blank"> Authenticate </a>'
      $('#result').html(auth_link);
    }
  });
});

function parse_time(date, hour, period) {
  if (period == 'PM') {
    hour = parseInt(hour)+12;
    hour = hour.toString();
  }
  date = date.split('/');
  temp = date[0];
  date[0] = date[2];
  date[2] = date[1]
  date[1] = temp;
  date = date.join('-');
  return date + 'T' + hour + ':00:00'
}
