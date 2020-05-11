const express = require('express');
var logger = require('morgan');
var mqtt_messenger = require("./utils/mqtt_messenger.js")
var database = require("./utils/database.js")

database.create_db();
mqtt_messenger.mqtt_receiver();
const app = express();
const port = process.env.PORT || "8000";


app.use(express.static(__dirname + '/public'));
app.use(logger('combined'));

app.get("/", (req, res) => {
  res.status(200).send("move to /index.html");
});

app.listen(port, () => {
  console.log(`Listening to requests on http://localhost:${port}`);
});
