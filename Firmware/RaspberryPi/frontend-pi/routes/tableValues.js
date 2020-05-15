var express = require('express');
var database = require("../utils/database.js")

var router = express.Router();

router.get('/values', function(req, res) {

  //get Minute Volume by getting sum of last minute delivered volume
  volumeData = database.get_volume();
  pressure = database.get_pressure();
  min_volume = 0
  for(var i = 0; i <= volumeData.length; i++) {
          min_volume = min_volume + volumeData[i][1];
  }
  max_pressure = 0
  for(var i = 0; i <= pressure.length; i++) {
          if (max_pressure < pressure[i][1]){
            max_pressure = pressure[i][1];
          }
  }
  res.json({
    "vt": database.get_vt(),
    "peak_pressure": max_pressure,
    "minute_volume": min_volume.toFixed(2),
  });
})

module.exports = router;
