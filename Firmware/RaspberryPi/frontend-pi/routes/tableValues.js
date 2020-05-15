var express = require('express');
var database = require("../utils/database.js")

var router = express.Router();

router.get('/values', function(req, res) {

  //get Minute Volume by getting sum of last minute delivered volume
  volumeData = database.get_volume();
  var min_volume = volumeData[1].reduce(function(a, b) {
    return a + b;
  }, 0);

  res.json({
    "vt": database.get_vt(),
    "peak_pressure": Math.max(database.get_pressure()),
    "minute_volume": min_volume,
  });
})

module.exports = router;
