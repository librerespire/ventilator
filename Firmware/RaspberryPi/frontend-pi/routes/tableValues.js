var express = require('express');
var database = require("../utils/database.js")

var router = express.Router();

router.get('/values', function(req, res) {
  res.json({
    "vt": database.get_vt(),
    "minute_volume": database.get_minute_volume(),
    "pip": database.get_pip(),
    "peep_calc": database.get_peep_calc(),
  });
})

module.exports = router;
