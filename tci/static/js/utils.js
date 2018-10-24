/**
 * Created by Administrator on 2018/9/27 0027.
 */
//进入vue
document.write("<script src='https://unpkg.com/vue/dist/vue.js'></script>");
//jquery
document.write("<script src='/static/jsery.min.js' type='text/javascript'></script>");
//utils
var utils = {
    //get请求
    get:function (url,resolve,reject) {
        $.get(url,function (data, textStatus, jqXHR) {
            resolve(data)
        },function (data, textStatus, jqXHR) {
            reject(data)
        })
    },
    //post请求
    post:function (url,data,resolve,reject) {
        return $.post(url,data,resolve,reject);
    }
}

