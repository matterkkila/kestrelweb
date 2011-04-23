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
      var server_stats = '';
      var queue_stats = '';

      for (server in data) {
        var s = data[server];
        var line = "<tr>";
        line += "<td>" + server + "</td>";
        line += "<td>" + s.server.version + "</td>";
        line += "<td>" + s.server.uptime + "</td>";
        line += "<td>" + s.server.time + "</td>";
        line += "<td>" + s.server.curr_connections + "</td>";
        line += "<td>" + s.server.total_connections + "</td>";
        line += "<td>" + s.server.curr_items + "</td>";
        line += "<td>" + s.server.total_items + "</td>";
        line += "<td>" + s.server.cmd_set + "</td>";
        line += "<td>" + s.server.cmd_get + "</td>";
        line += "<td>" + s.server.cmd_peek + "</td>";
        line += "<td>" + s.server.get_hits + "</td>";
        line += "<td>" + s.server.get_misses + "</td>";
        line += "<td>" + format_bytes(s.server.bytes_read) + "</td>";
        line += "<td>" + format_bytes(s.server.bytes_written) + "</td>";
        line += "</tr>";
        server_stats += line;

        for (queue in s.queues) {
          d = s.queues[queue];
          var q_line = "<tr>";
          q_line += "<td>" + server + "</td>";
          q_line += "<td>" + queue + "</td>";
          q_line += "<td>" + format_bytes(d.logsize) + "</td>";
          q_line += "<td>" + d.total_items + "</td>";
          q_line += "<td>" + d.expired_items + "</td>";
          q_line += "<td>" + d.items + "</td>";
          q_line += "<td>" + d.mem_items + "</td>";
          q_line += "<td>" + format_bytes(d.bytes) + "</td>";
          q_line += "<td>" + format_bytes(d.mem_bytes) + "</td>";
          q_line += "<td>" + d.age + "</td>";
          q_line += "<td>" + d.waiters + "</td>";
          q_line += "<td>" + d.open_transactions + "</td>";
          q_line += "</tr>";
          queue_stats += q_line;
        }
      }

      $('#server_stats').html(server_stats);
      $('#queue_stats').html(queue_stats);
    }
  });
};

$(document).ready(function() {
  get_stats();
  refresh = setInterval(get_stats, 5000);
});