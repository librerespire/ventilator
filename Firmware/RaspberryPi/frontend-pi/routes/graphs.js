var express = require('express');
var database = require("../utils/database.js")

var router = express.Router();

router.get('/pressure', function (req, res) {
  res.json({"data": database.get_pressure()});
})

router.get('/flowrate', function (req, res) {
  res.json({"data": database.get_flow_rate()});
})

router.get('/volume', function (req, res) {
  res.json({"data": database.get_volume()});
})

router.get('/time', function (req, res) {
  res.json({"data": database.get_time()});
})

module.exports = router;
