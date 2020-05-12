var express = require('express');
var mqtt_messenger = require("./utils/mqtt_messenger.js")

var router = express.Router();

const FIO2_CONFIG_TOPIC = 'Config/fio2'
const RR_CONFIG_TOPIC = 'Config/rr'
const PEEP_CONFIG_TOPIC = 'Config/peep'
const VT_CONFIG_TOPIC = 'Config/vt'
const IE_CONFIG_TOPIC = 'Config/ie'

router.put('/fio2', function (req, res) {
  console.log(FIO2_CONFIG_TOPIC, req.query.fio2);
  console.log("set fio2");
})

router.put('/rr', function (req, res) {
  console.log(RR_CONFIG_TOPIC, req.query.rr);
  console.log("set rr");
})

router.put('/vt', function (req, res) {
  console.log(VT_CONFIG_TOPIC, req.query.vt);
  console.log("set vt");
})

router.put('/peep', function (req, res) {
  console.log(PEEP_CONFIG_TOPIC, req.query.peep);
  console.log("set peep");
})

router.put('/ie', function (req, res) {
  console.log(IE_CONFIG_TOPIC, req.query.ie);
  console.log("set ie_ratio");
})

module.exports = router;
