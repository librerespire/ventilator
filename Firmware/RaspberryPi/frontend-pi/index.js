const express = require('express');
var logger = require('morgan');
var mqtt_messenger = require('./utils/mqtt_messenger.js');
var graphs = require('./routes/graphs.js');
var configs = require('./routes/configs.js');
var table = require('./routes/tableValues.js');

mqtt_messenger.mqtt_receiver();
const app = express();
const port = process.env.PORT || "8000";

app.use(express.static(__dirname + '/public'));
app.use(logger('combined'));
app.use('/api/graphs', graphs);
app.use('/api/configs', configs);
app.use('/api/table', table);

app.listen(port, () => {
  console.log(`Listening to requests on http://localhost:${port}`);
});
