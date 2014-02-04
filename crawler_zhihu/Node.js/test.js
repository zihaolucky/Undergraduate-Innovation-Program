//get request
var nodegrass = require('nodegrass'),
    request = require('request'),
    cheerio = require('cheerio'),
    http = require('http'),
	https=require("https"),
    url = require('url'),
	querystring = require("querystring");
	
var login_options = {
	host:'www.zhihu.com/login',
	method:"post",
	headers: {
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36'
	}
}

var login_password = '2241226',
    login_email = '137552789@qq.com';

var contents = querystring.stringify({
    'email':login_email,
    'password':login_password,
});
	

var options = {
	host:'www.zhihu.com/people/zihaolucky/followers',
	method:"post",
	headers:{
	    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
	    'Host':'www.zhihu.com',
	    'Origin':'http://www.zhihu.com',
	    'Connection':'keep-alive',
	    'Referrer':'http://www.zhihu.com/people/zihaolucky/followers',
	    'Content-Type':'application/x-www-form-urlencoded'
	}
}

var req=https.request(login_options,function(res){
	res.setEncoding("utf8");
	var headers=res.headers;
	var cookies=headers["set-cookie"];
	cookies.forEach(function(cookie){
		console.log(cookie);
	});
	res.on("data",function(data){
		console.log(data);
	});
});

req.write(contents);
req.end();


/*
nodegrass.get("http://www.zhihu.com/topic/19553176/top-answers",function(data,status,headers){
    console.log(status);
    //console.log(headers);
    //console.log(data);
	
	//urls = [];
	//urls.push(data.find(".question-link").text());
	//console.log(urls);
	
	var $ = cheerio.load(data);
	var urls = new Array();
	urls.push($('.question_link').attr('href'));
	//urls.push($('.question_link').attr('href'));
	console.log(urls);
	
},null,'utf8').on('error', function(e) {
    console.log("Got error: " + e.message);
});
*/