var express = require('express');
var database = require("../utils/database.js")

var router = express.Router();

router.get('/values', function (req, res) {
  res.json({"vt": database.get_vt()});
})

module.exports = router;
