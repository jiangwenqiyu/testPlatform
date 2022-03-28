
// 向table插入一空行
function insertTr() {
    // 如果没有用例则排序为1
    if ($("table tbody tr").length == 0) {

        $("table").append("<tr id='content-tr'>" +
            "<td class='index'>1</td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td></td>" +
            "<td></td>" +
            "<td></td>" +
            "<td><div><a href='javascript:;' onclick='savecase(this)'>保存</a></div><div><a href='javascript:;' onclick='runSingle(this);'>测试</a></div><div><a href='javascript:;' onclick='deleteCase(this);'>删除</a></div></td></tr>")

    }
    else
        {
        // 获取最后一行的排序，+1给添加的下一行
        maxOrder = parseInt($("table").find('tr:eq(' + ($("table tr").length - 1).toString() + ')').find('td:eq(0)').text()) + 1;

        $("table").append("<tr id='content-tr'>" +
            "<td class='index'>" + maxOrder + "</td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td contenteditable='true'></td>" +
            "<td></td>" +
            "<td></td>" +
            "<td></td>" +
            "<td><div><a href='javascript:;' onclick='savecase(this)'>保存</a></div><div><a href='javascript:;' onclick='runSingle(this);'>测试</a></div><div><a href='javascript:;' onclick='deleteCase(this);'>删除</a></div></td></tr>")
        }
}

// 向table插入数据
function insertData(caseOrder,caseName,casePath,caseHeader,param, caseData,caseDataType,exp,save,caseId, status, updateTime, caseReqType) {
    caseHeader = JSON.stringify(caseHeader);
    caseData = JSON.stringify(caseData);
    param = JSON.stringify(param);
    exp = JSON.stringify(exp);
    save = JSON.stringify(save);
    // 转换状态为中文
    if (status == '0' || status == null || status == '') {
        status = '就绪';
    }else if (status == '0') {

    }

    if (save == null) {
        save = '';
    }


    $("table").append("<tr id='content-tr' class='caseId-" + caseId + "'>" +
        "<td class='index'>" + caseOrder + "</td>" +
        "<td contenteditable='true'>" + caseName + "</td>" +
        "<td contenteditable='true'>" + casePath + "</td>" +
        "<td contenteditable='true'>" + caseHeader + "</td>" +
        "<td contenteditable='true'>" + param + "</td>" +
        "<td contenteditable='true'>" + caseData + "</td>" +
        "<td contenteditable='true'>" + caseDataType + "</td>" +
        "<td contenteditable='true'>" + caseReqType + "</td>" +
        "<td contenteditable='true'>" + exp + "</td>" +
        "<td contenteditable='true'>" + save + "</td>" +
        "<td></td>" +
        "<td>" + status + "</td>" +
        "<td>" + updateTime + "</td>" +
        "<td><div><a href='javascript:;' onclick='savecase(this)'>保存</a></div><div><a  href='javascript:;' onclick='runSingle(this);'>测试</a></div><div><a  href='javascript:;' onclick='deleteCase(this);'>删除</a></div></td></tr>");
}

function generateTable() {
    // 生成表格
    $("div").append("<table border='1' cellspacing='0' style='margin-top: 10px'></table>");
    $("table").append("<thead></thead>");
    $("thead").append("<tr></tr>");
    var title = ['序号','*用例名称', '*用例路径', '*请求头', 'params', '入参', '*入参类型', '*请求类型','*预期结果', '需要保存的对象', '返回值', '上次执行状态', '上次执行时间', '操作'];
    for (var i = 0; i < title.length; i++) {
        if (title[i] == '序号' || title[i] == '入参类型' || title[i] == '操作' || title[i] == '上次执行状态' || title[i] == '上次执行时间' || title[i] == '请求类型') {
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
                    insertData(data[i].caseOrder, data[i].name, data[i].path, data[i].header, data[i].param, data[i].data, data[i].dataType,data[i].exp_result,data[i].need_save,data[i].id, data[i].status, data[i].updateTime, data[i].dataReqType);
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
        data['id'] = c.replace('caseId-', '').replace(' ui-sortable-handle', '');
    }

    content = [];
    $(obj).parent().parent().parent().children().each(function (i) {
        temp = $.trim($(this).text());
        if (i in [1, 2, 3, 7]) {
            if (temp == null || temp == '') {
                alert('必填项不能为空！');
                throw '必填项不能为空';
            }
        }
        content.push(temp);
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

// 保存全部用例
function saveallcases() {
    data = [];
    $('tbody tr').each(function (i) {
        temp = {};
        content = [];
        $(this).children().each(function (j) {
            // 对文本首尾去除空白字符
            text = $(this).text().trim();
            // 判断必填项是否为空
            if (j in [1, 2, 3, 7] && (text == '' || text == null)) {
                alert('请检查必填项不能为空');
                throw '必填项不能为空';
            }
            // 判断是新增还是更新
            judge = $(this).parent().attr('class');
            if (judge == null) {  // 新增
                temp['updateType'] = 1;  // ui-sortable-handle
                temp['id'] = null;
            } else {             // 更新
                temp['updateType'] = 2;
                temp['id'] = judge.replace(' ui-sortable-handle', '').replace('caseId-', '');
            }
            // 获取三级类id
            temp['thirdId'] = localStorage.getItem('currentthirdId');

            // 构建content参数
            content.push(text);
            temp['content'] = content;
        });
        data.push(temp);
    });

    $.ajax({
        url:'/loginInfo/saveCases',
        type: 'post',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(data),
        success: function (resp) {
            if (resp.status != '0') {
                alert(resp.msg);
            } else {
                alert('保存成功！');
            }
        }
    });


}


// 给tr重新排序
function reOrder() {
    parseInt($("tbody tr").eq($("tbody tr").length - 1).text());
    $("tbody tr").each(function (i) {
        $(this).children('td:eq(0)').html(i+1);
    });

}


// 删除单行
function deleteCase(obj) {
    // 判断是否已经保存进数据库   留个bug 保存后如果不刷新页面，删除的时候默认判断为未保存的
    console.log($(obj).parent().parent().parent().attr('class'));
    cl = $(obj).parent().parent().parent().attr('class')
    if (cl == '' || cl == null) {
        $(obj).parent().parent().parent().remove();
        reOrder();
    }else if (cl.replace(' ui-sortable-handle', '') == '' || cl.replace(' ui-sortable-handle', '') == null) {
        $(obj).parent().parent().parent().remove();
        reOrder();
    } else {
        id = cl.replace(' ui-sortable-handle', '').replace('caseId-', '');  // 获取caseId，发送请求删除
    }

}


/*  执行测试用例的代码  */
// 执行单条测试用例
function runSingle(obj) {
    // 判断用例是否保存
    cl = $(obj).parent().parent().parent().attr('class');
    if (cl == null || cl == '') {
        alert('需要先保存刷新一下才能执行');
    }else if (cl.replace(' ui-sortable-handle', '') == '' || cl.replace(' ui-sortable-handle', '') == null) {
        alert('需要先保存刷新一下才能执行');
    } else {
        id = cl.replace('caseId-', '');
        $.ajax({
            url: '/loginInfo/runCases',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify([id]),
            success: function (resp) {
                $(obj).parent().parent().parent().children('td:eq(10)').html(JSON.stringify(resp));
            }
        });

    }
}




$(document).ready(function () {
    generateTable();

    // 双击可拖动,并排序
    $(document).on("dblclick", "tbody", function () {
        $("tbody").sortable({
            stop: function () {
                $('tbody tr').each(function (i) {
                    $(this).children().eq(0).text(i + 1);
                });
            }
        });
    });

    // 单击可编辑
    $(document).on("click", 'tbody',function () {
        $("tbody").sortable("destroy");
    });








});