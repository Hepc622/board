/**
 * Created by Administrator on 2017/12/5 0005.
 */
var Ajax = {
    get: function (url,resolve, reject) {
        var obj = new XMLHttpRequest();  // XMLHttpRequest对象
        obj.open('GET', url, true);
        obj.onreadystatechange = function () {
            Ajax.dealResponse(obj,resolve,reject)
        };
        obj.send();
    },
    post: function (url, data,resolve,reject) {
        var obj = new XMLHttpRequest();  // XMLHttpRequest对象
        obj.open("POST", url, true);
        obj.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        obj.setRequestHeader("Content-type", "application/json;charset=UTF-8");
        obj.onreadystatechange = function () {
            Ajax.dealResponse(obj,resolve,reject)
        };
        obj.send(JSON.stringify(data));// 发送post数据
    },
    dealResponse:function(obj,resolve,reject){
        // readyState == 4说明请求已完成
        if (obj.readyState == 4) {
            if (obj.status == 200 || obj.status == 304) {
                resolve(this.stringToJson(obj.responseText));//直接将对象传入
            } else {
                reject(this.stringToJson(obj.responseText));
            }
        }
    },
    //字符串转json如果是字符串不是json格式直接放回字符串，反之json
    stringToJson:function(str){
        try{
            return JSON.parse(str)
        }catch (Exception){
            return str
        }
    }
}
