var currentfirstId;
var currentsecondId;
var currentthirdId;

// 获取一级菜单内容:
function getFirst() {
    // 加载图标
    $("#first").append("<div style='height: 100px'><img src='/static/logo1.png' style='height: 100%;width: 100%'></div>");

    $.ajax(
        {
            url: "/loginInfo/getfirstlist",
            type: "post",
            contentType: 'application/json',
            dataType: 'json',
            success: function (resp) {
                if (resp.status == "0") {
                    firstInfo = resp.data;

                    ul = $("#first").append("<ul id='first-ul'></ul>");
                    for (var i = 0; i < firstInfo.length; i++) {
                        $("#first-ul").append("<li><a id=fir-" + firstInfo[i].first_id + " onclick='editFirstColor(this)'>"+firstInfo[i].first_name+"</a></li>")
                    }

                } else {
                    msg = resp.msg;
                }
            }
        }
    )
}



// 点击一级菜单，获取二级菜单内容: 清空二、三级内容  重置一级菜单颜色、修改选定菜单颜色、清空二级菜单内容、
function editFirstColor(obj) {
    // 先清空二级菜单
    $("#second").html('');
    // 清空三级内容
    $("#third-top").html('');
    $("#third-middle").html('');
    $("#third-content").html('');

    // 写入二级菜单
    var li = $("#first li");
    for (var i = 0; i < li.length; i++) {
        $(li[i]).css('backgroundColor', "#333333");
    }
    $(obj).parent().css('backgroundColor', 'green');
    var id = $(obj).attr("id");
    id = id.replace("fir-","");
    currentfirstId = id;
    localStorage.setItem("currentfirstId", currentfirstId);
    function getSecond() {
        req_data = {"firstId":id};
        $.ajax(
            {
                url: "/loginInfo/getsecondlist",
                type: "post",
                contentType: 'application/json',
                dataType: "json",
                data: JSON.stringify(req_data),
                success: function (resp) {
                    if (resp.status == "0") {
                        secondInfo = resp.data;
                        $("#second").append("<ul id='second-ul'></ul>");
                        for (var i = 0; i < secondInfo.length; i++) {
                            secondInfo[i].second_name
                            $("#second-ul").append("<li class='second-content'><a id='sec-" + secondInfo[i].second_id + "' class='second-content' onclick='editSecondColor(this)'>" + secondInfo[i].second_name + "</a></li>")
                        }
                    } else {
                        alert(resp.msg);
                    }
                }
            }
        );
    }
    getSecond();
    // 点击一级菜单的时候，自动获取二级菜单第一个的三级顶部，同时去掉标体数据

}



// 点击二级菜单，获取三级菜单内容：重置二级菜单颜色、修改选定菜单颜色、清空三级菜单内容、
function editSecondColor(obj) {
    // 先清空三级菜单
    // 清空三级内容
    $("#third-top").html('');
    $("#third-middle").html('');
    $("#third-content").html('');

    id = $(obj).attr('id');
    id = id.replace('sec-', '');
    currentsecondId = id;
    localStorage.setItem('currentsecondId', currentsecondId);
    req_data = {'secondId': id};

    // 获取三级菜单
    $.ajax({
        url: "/loginInfo/getthirdlist",
        type: "post",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(req_data),
        success: function (resp) {
            if (resp.status == '0') {
                thirdInfo = resp.data;
                // 写入三级菜单
                for (var i = 0; i < thirdInfo.length; i++) {
                    $("#third-top").append("<div id='third-" + thirdInfo[i].third_id + "' class='bord-style' onclick='editThirdColor(this)'>" + thirdInfo[i].third_name + "</div>");
                }
            } else {
                alert(resp.msg);
            }
        }
    });
}



// 点击三级菜单，获取表体内容
function editThirdColor(obj) {
    id = $(obj).attr('id');
    id = id.replace("third-", "");
    currentthirdId = id;
    localStorage.setItem("currentthirdId", currentthirdId);

    // 清空表体内容
    $("#third-content").html("");

    // 如果是压力测试的标签，进入到对应页面
    if ($(obj).html() == '压力测试') {
        $("#third-content").append("<iframe scrolling=\"yes\" src=\"/static/html/stressTest.html\" frameborder=\"0\" width=\"100%\" height=\"100%\"></iframe>");
    } else {
        // 嵌入iframe
        $("#third-content").append("<iframe scrolling=\"yes\" src=\"/static/html/testcase.html\" frameborder=\"0\" width=\"100%\" height=\"100%\"></iframe>");
    }





}



$(document).ready(function () {
    // 生成一级菜单
    getFirst();



});