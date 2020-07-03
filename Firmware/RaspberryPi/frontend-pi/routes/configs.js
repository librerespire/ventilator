var express = require('express');
var mqtt_messenger = require("../utils/mqtt_messenger.js")

var router = express.Router();

const CALIB_FLOW_RATE_CONFIG_TOPIC = 'Config/calib_flow_rate'
const FIO2_CONFIG_TOPIC = 'Config/fio2';
const RR_CONFIG_TOPIC = 'Config/rr';
const PEEP_CONFIG_TOPIC = 'Config/peep';
const VT_CONFIG_TOPIC = 'Config/vt';
const IE_CONFIG_TOPIC = 'Config/ie';
const PMAX_CONFIG_TOPIC = 'Config/pmax';
const PIP_CONFIG_TOPIC = 'Config/pip';
const MINUTE_VOL_CONFIG_TOPIC = 'Config/mv';
const MODE_CONFIG_TOPIC = 'Config/mode';

router.get('/calib_flow_rate', function (req, res) {
  mqtt_messenger.mqtt_sender(CALIB_FLOW_RATE_CONFIG_TOPIC, req.query.calib_flow_rate);
  res.sendStatus(200);
})

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
  mqtt_messenger.mqtt_sender(IE_CONFIG_TOPIC, req.query.ie);
  res.sendStatus(200);
})

router.get('/pmax', function (req, res) {
  mqtt_messenger.mqtt_sender(PMAX_CONFIG_TOPIC, req.query.pmax);
  res.sendStatus(200);
})

router.get('/pip', function (req, res) {
  mqtt_messenger.mqtt_sender(PIP_CONFIG_TOPIC, req.query.pip);
  res.sendStatus(200);
})

router.get('/mv', function (req, res) {
  mqtt_messenger.mqtt_sender(MINUTE_VOL_CONFIG_TOPIC, req.query.mv);
  res.sendStatus(200);
})

router.get('/mode', function (req, res) {
    mqtt_messenger.mqtt_sender(MODE_CONFIG_TOPIC, req.query.mode);
    res.sendStatus(200);
})

module.exports = router;
