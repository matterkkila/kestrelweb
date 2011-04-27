var format_bytes = function(val_bytes) {
  var new_val = 0;
  var suffix = '';

  if (val_bytes > 1073741824) {
    new_val = val_bytes / 1073741824;
    suffix = 'GB';
  } else if (val_bytes > 1048576) {
    new_val = val_bytes / 1048576;
    suffix = 'MB';
  } else if (val_bytes > 1024) {
    new_val = val_bytes / 1024;
    suffix = 'KB';
  } else {
    new_val = val_bytes;
    suffix = 'B';
  }

  return  new_val.toFixed(2) + ' ' + suffix;
};

var get_stats = function() {
  $.ajax({
    url: '/ajax/stats.json',
    dataType: 'jsonp',
    data: {
      servers: $('#servers').val()
    },
    success: function(data, textStatus, jqXHR) {
        $('#content').html(mustache.tmpl_content(data));
    }
  });
};

$(document).ready(function() {
  get_stats();
  setInterval(get_stats, parseInt($('#refresh').val()));
});