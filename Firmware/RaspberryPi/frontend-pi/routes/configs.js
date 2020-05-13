var express = require('express');
var mqtt_messenger = require("../utils/mqtt_messenger.js")

var router = express.Router();

const FIO2_CONFIG_TOPIC = 'Config/fio2';
const RR_CONFIG_TOPIC = 'Config/rr';
const PEEP_CONFIG_TOPIC = 'Config/peep';
const VT_CONFIG_TOPIC = 'Config/vt';
const IE_CONFIG_TOPIC = 'Config/ie';

router.get('/fio2', function (req, res) {
  mqtt_messenger.mqtt_sender(FIO2_CONFIG_TOPIC, req.query.fio2);
  res.sendStatus(200);
})

router.get('/rr', function (req, res) {
  mqtt_messenger.mqtt_sender(RR_CONFIG_TOPIC, req.query.rr);
  res.sendStatus(200);
})

router.get('/vt', function (req, res) {
  mqtt_messenger.mqtt_sender(VT_CONFIG_TOPIC, req.query.vt);
  res.sendStatus(200);
})

router.get('/peep', function (req, res) {
  mqtt_messenger.mqtt_sender(PEEP_CONFIG_TOPIC, req.query.peep);
  res.sendStatus(200);
})

router.get('/ie', function (req, res) {
  mqtt_messenger.mqtt_sender(IEI_CONFIG_TOPIC, req.query.ie);
  res.sendStatus(200);
})

module.exports = router;
