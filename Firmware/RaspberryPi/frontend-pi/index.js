const express = require('express');
var logger = require('morgan');
var mqtt_messenger = require("./utils/mqtt_messenger.js")
var graphs = require('./routes/graphs.js');

mqtt_messenger.mqtt_receiver();
const app = express();
const port = process.env.PORT || "8000";

app.use(express.static(__dirname + '/public'));
app.use(logger('combined'));
app.use('/api/graphs', graphs);

app.get("/", (req, res) => {
  res.status(200).send("move to /index.html");
});

app.listen(port, () => {
  console.log(`Listening to requests on http://localhost:${port}`);
});
