var express = require('express');
var database = require("../utils/database.js")

var router = express.Router();

router.get('/values', function(req, res) {

  //return the latest values
  res.json({
    "vt": database.get_vt(),
    "minute_volume": database.get_minute_volume(),
    "peak_pressure": database.get_pip(),
  });
})

module.exports = router;
