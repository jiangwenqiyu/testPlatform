
// 向table插入一空行
function insertTr() {
    $("table").append("<tr id='content-tr'>" +
        "<td></td>" +
        "<td contenteditable='true'></td>" +
        "<td contenteditable='true'></td>" +
        "<td contenteditable='true'></td>" +
        "<td contenteditable='true'></td>" +
        "<td contenteditable='true'></td>" +
        "<td contenteditable='true'></td>" +
        "<td contenteditable='true'></td>" +
        "<td contenteditable='true'></td>" +
        "<td contenteditable='true'></td>" +
        "<td><div><a href='javascript:;' onclick='savecase(this)'>保存</a></div><div><a class='exe' href=''>测试</a></div><div><a href=''>删除</a></div></td></tr>")
}

// 向table插入数据
function insertData(caseOrder,caseName,casePath,caseHeader,param, caseData,caseDataType,exp,save,caseId) {
    caseHeader = JSON.stringify(caseHeader);
    caseData = JSON.stringify(caseData);
    param = JSON.stringify(param);
    exp = JSON.stringify(exp);
    save = JSON.stringify(save);
    if (save == null) {
        save = '';
    }


    $("table").append("<tr id='content-tr' class='caseId-" + caseId + "'>" +
        "<td>" + caseOrder + "</td>" +
        "<td contenteditable='true'>" + caseName + "</td>" +
        "<td contenteditable='true'>" + casePath + "</td>" +
        "<td contenteditable='true'>" + caseHeader + "</td>" +
        "<td contenteditable='true'>" + param + "</td>" +
        "<td contenteditable='true'>" + caseData + "</td>" +
        "<td contenteditable='true'>" + caseDataType + "</td>" +
        "<td contenteditable='true'>" + exp + "</td>" +
        "<td contenteditable='true'>" + save + "</td>" +
        "<td contenteditable='true'></td>" +
        "<td><div><a href='javascript:;' onclick='savecase(this)'>保存</a></div><div><a href=''>测试</a></div><div><a href=''>删除</a></div></td></tr>");
}

function generateTable() {
    // 生成表格
    $("div").append("<table border='1' cellspacing='0'></table>");
    $("table").append("<tr></tr>");
    var title = ['序号','*用例名称', '*用例路径', '*请求头', 'params', '入参', '*入参类型', '*预期结果', '需要保存的对象', '返回值', '操作'];
    for (var i = 0; i < title.length; i++) {
        if (title[i] == '序号' || title[i] == '入参类型' || title[i] == '操作') {
            $("tr").append("<td class='short'>" + title[i] + "</td>");
        } else if (title[i] == '用例名称' || title[i] == '预期结果' || title[i] == '需要保存的对象') {
            $("tr").append("<td class='middle'>" + title[i] + "</td>");
        } else {
            $("tr").append("<td class='long'>" + title[i] + "</td>");
        }
    }
    // 从接口获取数据, 插入到表体中
    var data = {'thirdId': localStorage.getItem('currentthirdId')};
    $.ajax({
        url: '/loginInfo/getCases',
        type: 'post',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(data),
        success: function (resp) {
            if (resp.status != '0') {
                alert(resp.msg);
            } else {
                data = resp.data;
                for (var i = 0; i < data.length; i++) {
                    insertData(data[i].caseOrder, data[i].name, data[i].path, data[i].header, data[i].param, data[i].data, data[i].dataType,data[i].exp_result,data[i].need_save,data[i].id);
                }
            }
        }
    });
}

// 保存单条用例
function savecase(obj) {
    var data = {};
    // 判断当前tr的class是否有caseId-  如果有，只需更新，如果没有，则需要插入数据
    c = $(obj).parent().parent().parent().attr('class');
    if (c == null) {
        data['updateType'] = 1; // 插入数据
    } else {
        data['updateType'] = 2; // 更新数据
        data['id'] = c.replace('caseId-', '');
    }

    content = [];
    $(obj).parent().parent().parent().children().each(function (i) {

        if (i in [1, 2, 3, 7]) {
            if ($.trim($(this).text()) == null || $.trim($(this).text()) == '') {
                alert('必填项不能为空！');
                throw '必填项不能为空';
            }
        }
        content.push($(this).text());
    });
    // 把遍历的结果传入data
    data['content'] = content;
    // 把三级模块id传入data
    console.log(localStorage.getItem('currentthirdId'));
    data['thirdId'] = localStorage.getItem('currentthirdId');


    $.ajax({
        url:'/loginInfo/saveCases',
        type: 'post',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify([data]),
        success: function (resp) {
            if (resp.status != '0') {
                alert(resp.msg);
            } else {
                alert('保存成功！');
            }
        }
    });



}


$(document).ready(function () {
    generateTable();

});