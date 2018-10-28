/**
 * Created by Administrator on 2018/9/27 0027.
 */
 document.write('<script src="/static/js/jquery.min.js"></script>')
 document.write("<script src='/static/js/vue/vue.js' type='text/javascript'></script>")
//utils
var utils = {
    //get请求
    get:function (url,resolve,reject) {
        $.ajax({
                url: url,
                type: "get",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                data: {},
                success: function (res) {
                    resolve(res)
                },
                error: function (res) {
                    reject(res)
                }
            });
    },
    //post请求
    post:function (url,data,resolve,reject) {
        $.ajax({
                url: url,
                type: "post",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(data),
                success: function (res) {
                    resolve(res)
                },
                error: function (res) {
                    reject(res)
                }
            });
    }
}

