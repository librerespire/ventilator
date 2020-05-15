var express = require('express');
var database = require("../utils/database.js")

var router = express.Router();

router.get('/values', function(req, res) {

  //get Minute Volume by getting sum of last minute delivered volume
  volumeData = database.get_volume();
  min_volume = 0
  for(var i = 0; i < volumeData.length; i++) {
          min_volume = min_volume + volumeData[i][1];
  }

  res.json({
    "vt": database.get_vt(),
    "peak_pressure": Math.max(database.get_pressure()),
    "minute_volume": min_volume,
  });
})

module.exports = router;
