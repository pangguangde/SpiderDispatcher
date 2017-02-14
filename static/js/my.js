/**
 * Created by pangguangde on 2017/1/15.
 */
function show_notify(msg_type, msg, delay) {
    $.bootstrapGrowl(msg, {
        type: msg_type,
        align: 'center',
        width: 'auto',
        delay: delay,
        offset: {from: 'top', amount: 5}
    });
}

function add_scheduler(spider_name) {
    var start_time = document.getElementById(spider_name + "_start").value;
    var interval = document.getElementById(spider_name + "_interval").value;
    var params = document.getElementById(spider_name + "_params").value;
    $.ajax({
        url: '/add_schedule?spider_name=' + spider_name + '&start_time=' + start_time + '&interval=' + interval + '&params=' + params,
        success: function (data) {
            if (data == 'success') {
                show_notify('success', spider_name + ': add schedule success!', 1000);
            } else {
                show_notify('danger', spider_name + ': add schedule failure!', 1500);
            }
        },
        error: function () {
            show_notify('danger', spider_name + ': 出错了!', 1500);
        }
    });
}

function run_spider(spider_name) {
    var params = document.getElementById(spider_name + "_params").value;
    $.ajax({
        url: '/add_job?spider_name=' + spider_name + "&params=" + params,
        success: function (data) {
            if (data == 'success') {
                show_notify('success', spider_name + ': is running now!', 1000);
            } else {
                show_notify('danger', spider_name + ': running failure!', 1500);
            }
        },
        error: function () {
            show_notify('danger', spider_name + ': 出错了!', 1500);
        }
    });
}

document.getElementById("header").innerHTML =
    "<div style=\"background: rgb(132, 31, 11);box-shadow:1px 1px 5px #523838;\">" +
        "<p class=\"slideShine\">" +
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SpiderDispatcher" +
        "</p>" +
    "<a style='float: right;margin-top: -20px;text-decoration: none' class='slideShine_b' href='https://github.com/pangguangde/SpiderDispatcher'>Fork me on Github - SpiderDispatcher&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a>" +
    "</div>";

// function show_notify(msg_type, msg, delay) {
//     $.bootstrapGrowl(msg, {
//         type: msg_type,
//         align: 'center',
//         width: 'auto',
//         delay: delay,
//         offset: {from: 'top', amount: 5},
//     });
// }

function cancel_spider(spider_name, job_id) {
    $.ajax({
        url: '/cancel/' + job_id,
        success: function (data) {
            if (data == 'success') {
                show_notify('success', spider_name + '(' + job_id + ')' + ': was cancelled!', 1000);
            } else {
                show_notify('danger', spider_name + '(' + job_id + ')' + ': cancel failure!', 1500);
            }
        },
        error: function () {
            show_notify('danger', spider_name + '(' + job_id + ')' + ': 出错了!', 1500);
        }
    });
}

// function show_notify(msg_type, msg, delay) {
//     $.bootstrapGrowl(msg, {
//         type: msg_type,
//         align: 'center',
//         width: 'auto',
//         delay: delay,
//         offset: {from: 'top', amount: 5}
//     });
// }

function pause_schedule(sche_id, spider_name) {
    $.ajax({
        url: '/pause_schedule?sche_id=' + sche_id,
        success: function (data) {
            if (data == 'success') {
                var element = document.getElementById(sche_id);
                element.setAttribute('onclick', 'resume_schedule(\'' + sche_id + '\', \'' + spider_name + '\')');
                element.setAttribute('class', 'btn btn-success');
                element.value = 'resume';
                $('#'+sche_id+'_status').text('paused');
                show_notify('success', spider_name + '(' + sche_id + ')' + ': was paused!', 1000);
            } else {
                show_notify('danger', spider_name + '(' + sche_id + ')' + ': pause failure!', 1500);
            }
        },
        error: function () {
            show_notify('danger', spider_name + '(' + sche_id + ')' + ': 出错了!', 1500);
        }
    });
}

function resume_schedule(sche_id, spider_name) {
    $.ajax({
        url: '/resume_schedule?sche_id=' + sche_id,
        success: function (data) {
            if (data == 'success') {
                var element = document.getElementById(sche_id);
                element.setAttribute('onclick', 'pause_schedule(\'' + sche_id + '\', \'' + spider_name + '\')');
                element.setAttribute('class', 'btn btn-warning');
                element.value = 'pause';
                $('#'+sche_id+'_status').text('running');
                show_notify('success', spider_name + '(' + sche_id + ')' + ': was resumed!', 1000);
            } else {
                show_notify('danger', spider_name + '(' + sche_id + ')' + ': resume failure!', 1500);
            }
        },
        error: function () {
            show_notify('danger', spider_name + '(' + sche_id + ')' + ': 出错了!', 1500);
        }
    });
}

function del_schedule(sche_id, spider_name) {
    $.ajax({
        url: '/del_schedule?sche_id=' + sche_id,
        success: function (data) {
            if (data == 'success') {
                document.getElementById(sche_id+'_tr').setAttribute('style', 'display:None');
                show_notify('success', spider_name + '(' + sche_id + ')' + ': was removed!', 1000);
            } else {
                show_notify('danger', spider_name + '(' + sche_id + ')' + ': remove failure!', 1500);
            }
        },
        error: function () {
            show_notify('danger', spider_name + '(' + sche_id + ')' + ': 出错了!', 1500);
        }
    });
}