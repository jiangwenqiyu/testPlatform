


function generateTable() {
    $("div").append("<table cell></table>");
    $("table").append("<tr></tr>");
    var title = ['序号','用例名称', '用例路径', '入参', '入参类型', '预期结果', '需要保存的对象','需要引用的值', '返回值'];
    for (var i = 0; i < title.length; i++) {
        if (title[i] == '序号') {
            $("tr").append("<td contenteditable='true' width='50px'>" + title[i] + "</td>");
        } else {
            console.log(i)
            $("tr").append("<td contenteditable='true' width='800px'>" + title[i] + "</td>");
        }

    }


}

$(document).ready(function () {
    generateTable();
});