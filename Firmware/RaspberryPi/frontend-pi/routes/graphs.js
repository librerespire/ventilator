var express = require('express');
var database = require("../utils/database.js")

var router = express.Router();

router.get('/pressure', function (req, res) {
  res.send(JSON.stringify(database.get_pressure()));
})

router.get('/flowrate', function (req, res) {
  res.send(JSON.stringify(database.get_flow_rate()));
})

router.get('/volume', function (req, res) {
  res.send(JSON.stringify(database.get_volume()));
})

module.exports = router;
