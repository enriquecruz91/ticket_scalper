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

function post_to(url, data) {
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

$('.post_to').live('click', function() {
  var data_route = $(this).data('funct');
  var data = get_data(data_route);
  var url = $(this).attr('href');
  post_to(url, data);
  return false;
});

$('.search_in').live('click', function() {
  var target = '#' + $(this).data('target');
  var query = $(target).val();
  iframe_search(query, 'ticketmaster');
  iframe_search(query, 'stubhub');
  return false
});
$('.search-input').live('keypress', function(e) {
  if(e.which == 13){
    $('.search_in').click();
  }
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
