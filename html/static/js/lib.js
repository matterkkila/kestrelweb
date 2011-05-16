var format_numeric = function(nStr, render) {
    nStr = render(nStr);
    var prefix = prefix || '';
    nStr += '';
    x = nStr.split('.');
    x1 = x[0];
    x2 = x.length > 1 ? '.' + x[1] : '';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1))
        x1 = x1.replace(rgx, '$1' + ',' + '$2');
    return prefix + x1 + x2;
};

var format_bytes = function(val_bytes, render) {
    var new_val = 0;
    var suffix = '';

    val_bytes = parseInt(render(val_bytes));

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

    return  new_val.toFixed(2) + '&nbsp;<small>' + suffix + '</small>';
};

var get_stats = function() {
    var server_list = [];
    $('#servers_content tr[x-kestrel-server]').each(function(i) {
        server_list[i] = $(this).attr('x-kestrel-server');
    });

    $.ajax({
        url: '/ajax/stats.json',
        dataType: 'jsonp',
        timeout: 1000,
        data: {
            servers: server_list.join(','),
            qsort: $('#qsort option:selected').val(),
            qreverse: $('#qreverse option:selected').val(),
            qfilter: $('#qfilter').val(),
        },
        success: function(data, textStatus, jqXHR) {
            $('#servers_content').html(mustache.servers({
                'servers': data['servers'],
                'size': function() {
                    return format_bytes;
                },
                'numeric': function() {
                    return format_numeric;
                }
            }));
            $('#queues_content').html(mustache.queues({
                'queues': data['queues'],
                'size': function() {
                    return format_bytes;
                },
                'numeric': function() {
                    return format_numeric;
                }
            }));
            $('#error_count').html(0);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $('#error_count').html(parseInt($('#error_count').html()) + 1);
        },
    });
};

$(document).ready(function() {
    //Load the mustache templates from the server
    var refresh_int = null;

    $.getJSON('/ajax/config.json', function (data) {
        $.each(data.templates, function (name, template) {
            mustache.addTemplate(name, template);
        });
        $('#content').html(mustache.content());
        $('#servers_content').html(mustache.servers({'servers': data.servers}));
        get_stats();
        refresh_int = setInterval(get_stats, parseInt($('#refresh').val()) * 1000);
        /* col header tooltips */
        $('.kw_table th').tipTip({
            defaultPosition: 'top',
            delay: 1000       
        });
    });

    $('#btn_refresh').live('click', function (e) {
        e.preventDefault();
        var button = $(this);
        if (!button.hasClass('paused')) {
            button.addClass('paused').html('Resume updates')
            clearInterval(refresh_int);
        } else {
            button.removeClass('paused').html('Pause updates');
            get_stats();
            refresh_int = setInterval(get_stats, parseInt($('#refresh').val()) * 1000);
        }
    });

    $('a.cmd').live('click', function() {
        var action = $(this).attr('x-kestrel-action');
        var row = $(this).closest('tr');
        var server = row.attr('x-kestrel-server');
        var queue = row.attr('x-kestrel-queue');
        var server_queue = server;
        if (queue) {
            server_queue = server_queue + ',' + queue
        }

        if (confirm(action + ' ' + server_queue)) {
            $.ajax({
                url: '/ajax/action.json',
                dataType: 'jsonp',
                data: {
                    'action': action,
                    'server': server_queue,
                },
                success: function(data, textStatus, jqXHR) {
                    if (action == 'delete') {
                        row.hide();
                    }
                    alert(data.results);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log(jqXHT);
                    console.log(textStats);
                    console.log(errorThrown);
                    alert('An error occurred');
                }
            });
        }
        return false;
    });
    
    /* sorting via col headers */
    var currentSort = 0;
    $('#kw_queues th a.sort').live('click',function(e) {
        e.preventDefault();
        var colHead         = $(this).closest('th');
        var sortOptions     = $('#qsort option');
        var reverseOptions  = $('#qreverse option');
        var cols            = $('#kw_queues th a.sort');
        var colIndex        = $.inArray(this,cols);
        if (colIndex != currentSort) {
            currentSort = colIndex;
            $(sortOptions[colIndex]).attr('selected','selected').siblings().removeAttr('selected');
            reverseOptions.removeAttr('selected');
            $(reverseOptions[0]).attr('selected','selected');
            colHead.addClass('current_sort').siblings().removeClass('current_sort').removeClass('reversed');
        } else {
            if($(reverseOptions[0]).attr('selected')) {
                $(reverseOptions[0]).removeAttr('selected').siblings().attr('selected','selected');
                colHead.addClass('reversed');
            } else {
                $(reverseOptions[1]).removeAttr('selected').siblings().attr('selected','selected');
                colHead.removeClass('reversed');
            }
        }
        get_stats();
    });

    /* toggle display of sections */
    $('#kw_sections input[type="checkbox"]').live('change',function(e) {
        var contentTriggers = $('#kw_sections input[type="checkbox"]');
        var content         = $('section.kw_section').hide();
        $.each(contentTriggers, function(k,v) {
            var checkbox = $(v);
            var foo  = $(content[k]);
            if (v.checked) {
                foo.show();
            }
        });
    });
});
