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
    $.ajax({
        url: '/add_schedule?spider_name=' + spider_name + '&start_time=' + start_time + '&interval=' + interval,
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
    $.ajax({
        url: '/add_job/' + spider_name,
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

document.getElementById("header").innerHTML = "<style> \.slideShine {width: 100%;font-size: 60px;text-align: left;background: #636060 -webkit-linear-gradient(left, #636060, #fff) 0 0 no-repeat;-webkit-background-size: 120px;-webkit-background-clip: text;-webkit-text-fill-color: rgba(0,0,0,0.2);-webkit-animation: slideShine 4s infinite;}@-webkit-keyframes slideShine {0% {background-position: 0 0;}100% {background-position: 100% 100%;}}</style><div style=\"background: rgb(132, 31, 11);\"><h1 class=\"slideShine\" style=\"margin-top: 0;margin-bottom: 0; padding-top:10px; padding-bottom:10px;box-shadow:1px 1px 5px #523838;\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SpiderDispatcher</h1></div>";

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