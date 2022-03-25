

function getFirst() {
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



// 清空二、三级内容  重置一级菜单颜色、修改选定菜单颜色、清空二级菜单内容、获取二级菜单内容
function editFirstColor(obj) {
    // 先清空二级菜单
    $("#second").html('');
    // 清空三级内容

    // 写入二级菜单
    var li = $("#first li");
    for (var i = 0; i < li.length; i++) {
        $(li[i]).css('backgroundColor', "#333333");
    }
    $(obj).parent().css('backgroundColor', 'green');
    var id = $(obj).attr("id");
    id = id.replace("fir-","");
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
    // 自动获取二级第一个的三级内容

}


// 重置二级菜单颜色、修改选定菜单颜色、清空三级菜单内容、获取三级菜单内容
function editSecondColor(obj) {
    // 先清空三级菜单
    $("#top-bord").html('');

    id = $(obj).attr('id');
    id = id.replace('sec-', '');
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
                    $("#top-bord").append("<div class='bord-style'>" + thirdInfo[i].third_name + "</div>");
                }
            } else {
                alert(resp.msg);
            }
        }
    });





}


$(document).ready(function () {
    // 生成一级菜单
    getFirst();


});