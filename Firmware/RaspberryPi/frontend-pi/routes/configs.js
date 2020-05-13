var express = require('express');
var mqtt_messenger = require("../utils/mqtt_messenger.js")

var router = express.Router();

const FIO2_CONFIG_TOPIC = 'Config/fio2';
const RR_CONFIG_TOPIC = 'Config/rr';
const PEEP_CONFIG_TOPIC = 'Config/peep';
const VT_CONFIG_TOPIC = 'Config/vt';
const IEE_CONFIG_TOPIC = 'Config/iee';
const IEI_CONFIG_TOPIC = 'Config/iei';

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

router.get('/iei', function (req, res) {
  mqtt_messenger.mqtt_sender(IEI_CONFIG_TOPIC, req.query.iei);
  res.sendStatus(200);
})

router.get('/iee', function (req, res) {
  mqtt_messenger.mqtt_sender(IEE_CONFIG_TOPIC, req.query.iee);
  res.sendStatus(200);
})

module.exports = router;
