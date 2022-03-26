
// 向table插入一空行
function insertTr() {
    $("table").append("<tr id='content-tr'><td></td><td contenteditable='true'></td><td contenteditable='true'></td><td contenteditable='true'></td><td contenteditable='true'></td><td contenteditable='true'></td><td contenteditable='true'></td><td contenteditable='true'></td><td contenteditable='true'></td><td><div><a href=''>保存</a></div><div><a href=''>测试</a></div><div><a href=''>删除</a></div></td></tr>")
}

// 向table插入数据
function insertData(caseOrder,caseName,casePath,caseHeader,caseData,caseDataType,exp,save) {
    caseHeader = JSON.stringify(caseHeader);
    caseData = JSON.stringify(caseData);

    $("table").append("<tr id='content-tr'>" +
        "<td>" + caseOrder + "</td>" +
        "<td contenteditable='true'>" + caseName + "</td>" +
        "<td contenteditable='true'>" + casePath + "</td>" +
        "<td contenteditable='true'>" + caseHeader + "</td>" +
        "<td contenteditable='true'>" + caseData + "</td>" +
        "<td contenteditable='true'>" + caseDataType + "</td>" +
        "<td contenteditable='true'>" + exp + "</td>" +
        "<td contenteditable='true'>" + save + "</td>" +
        "<td contenteditable='true'></td>" +
        "<td><div><a href=''>保存</a></div><div><a href=''>测试</a></div><div><a href=''>删除</a></div></td></tr>")
}

function generateTable() {
    // 生成表格
    $("div").append("<table border='1' cellspacing='0'></table>");
    $("table").append("<tr></tr>");
    var title = ['序号','*用例名称', '*用例路径', '*请求头', '入参', '*入参类型', '*预期结果', '需要保存的对象', '返回值', '操作'];
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
                    insertData(data[i].caseOrder, data[i].caseName, data[i].casePath, data[i].caseHeader, data[i].caseData, data[i].caseDataType,0,0);
                }
            }
        }
    });



}


$(document).ready(function () {
    generateTable();
});