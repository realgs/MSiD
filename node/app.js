var express = require('express');
var http = require('http');

var app = express();

require('./routes')(app);

http.createServer(app).listen("8080", (err) => {
  if (!err) {
    console.log("ok");
  }
});