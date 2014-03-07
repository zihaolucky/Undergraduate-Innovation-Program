//app.js

var http = require('http');

http.createServer(function(req, res) {
	res.writeHead(200, {'Content-Type':'text/html'});
	res.write('<h1>Node.js</h1>');
	res.write("<h2>It's my first Node.js program!</h2>");
	res.end('<p>Hello world.</p>');
}).listen(3000);
console.log("HTTP Server is listening at port 3000.");