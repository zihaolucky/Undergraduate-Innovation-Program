var request = require('request'),
    cheerio = require('cheerio'),
    http = require('http'),
    url = require('url');
//用逗号分隔用户名
var userarray = "zihaolucky";

 
var users = userarray.split(',');
var usercursor = 0;
// insert the followers_number
var result = new Array();
var showtable = true;
var cardcount = 0;
 
function showmsg(msg) { console.log(msg); }
function showresult() {
    for (i in result) {
		console.log(result[i].name)
	}
}

 
function loadmore() {
    var content = $("#tempframe").contents();
    var name = content.find(".title-section.ellipsis a").html();
    if (content.find('.zu-button-more[aria-role]').length < 1) {
        showmsg(name + "的" + cardcount + "个关注者加载完成");
        showratio();
    }
    else {
        content.find('.zu-button-more[aria-role]').get(0).click();
        var total = content.find(".zm-profile-side-following strong").html();
        cardcount = content.find('.zm-profile-card .zm-list-content-medium').length;
        console.log("正在加载" + name + "的关注者:" + cardcount + "/" + total + "... <img style='vertical-align: text-bottom;'/>");
        // 设置Timeout为1000的速度较快
		setTimeout(loadmore, 1000);
    }
}
 
function showratio() {
    var cards = $("#tempframe").contents().find('.zm-profile-card .zm-list-content-medium');
    cards.each(function () {
        var name = $(this).find('a.zg-link').html();
        var id = $(this).find('a.zg-link').attr("href").replace("http://www.zhihu.com/people/", "");
		
		//控制部分,将获得的所有信息都一并存入;调用addresult()函数
        if (true) {
            var r = new Object();
            r.name = name;
            r.id = id;
            addresult(r);
        }
    });
    showresult();
    usercursor++;
    loaduser();
}
 
function loaduser() {
    if (usercursor < users.length) {
        showmsg("共" + users.length + "个用户，准备扫描第" + (usercursor + 1) + "个...");
        $("#tempframe").attr("src", "/people/" + users[usercursor] + "/followers");
    }
    else {
        showmsg("所有" + users.length + "名用户的关注者已经全部扫描完成，共找到" + result.length + "个符合条件的用户");
    }
}
 
function addresult(r) {
    var exist = false;
	showmsg("共" + users.length + "个用户，准备扫描第" + (usercursor + 1) + "个...");
    //for (i in result) { if (r.id == result[i].id) { exist = true; break; } } 查重,事实上这并不需要
    if (!exist) result.push(r);
}
 

$("#tempframe").load(function () { loadmore(); });
loaduser();