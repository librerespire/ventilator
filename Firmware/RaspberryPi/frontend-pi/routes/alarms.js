var express = require('express');
var database = require("../utils/database.js")

var router = express.Router();

router.get('/major', function(req, res) {
  major_alarms = database.get_major_alarm();
  res.json(major_alarms);
})

router.get('/minor', function(req, res) {
  minor_alarm = database.get_minor_alarm();
  res.json(minor_alarm);
})

module.exports = router;
