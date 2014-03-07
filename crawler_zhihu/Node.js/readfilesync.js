// readfilesync.js

var fs = require('fs');
var data = fs.readFileSync('zihaolucky.txt', 'utf-8');

console.log(data);
console.log('end.');