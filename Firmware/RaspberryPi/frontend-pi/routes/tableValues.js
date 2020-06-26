var express = require('express');
var database = require("../utils/database.js")

var router = express.Router();

router.get('/values', function(req, res) {
  res.json({
    "vt": database.get_vt(),
    "minute_volume": database.get_minute_volume(),
    "pip": database.get_pip(),
  });
})

router.get('/alarms/major', function(req, res) {
  major_alarms = database.get_major_alarm();
  res.json(major_alarms);
})

router.get('/alarms/minor', function(req, res) {
  minor_alarm = database.get_minor_alarm();
  res.json(minor_alarm);
})

module.exports = router;
