## The design

The design of the ventilator is based on the minimum standards published by the British government [here](https://www.gov.uk/government/publications/coronavirus-covid-19-ventilator-supply-specification/rapidly-manufactured-ventilator-system-specification)


## Objectives

- Design a ventilator composed of mechanical components freely available in most
regions of the world.
- Design a ventilator without the use of a Bellow or a “Bag”, which is either not
available or limited in number in an emergency situation.
- Minimize the use of mechanically moving components to increase durability.
- Easily sourced and easily assembled by a technician with limited medical
knowledge with off-the-shelf components.
- Option to use “Wall” oxygen / oxygen cylinders or a combination.
- Retain the capability to tolerate significant pressure difference or fluctuations.
- Be effective while retaining all the safety features.
- Maintain total cost of manufacture of the ventilator within affordable range,
especially to support developing countries.
- Use a programmable chip as a microcontroller which is a cheaper option yet be
powerful enough for real-time calculations.
- Use a visual aid (LCD) which is informative as well as user friendly.
- Ensuring a safe, reliable and robust design on par with industry standards.


## Functional specification

- Functional Modes
a. Pressure control Continuous Mandatory Ventilation (PC- CMV)
b. Pressure control Intermittent Mandatory Ventilation (PC-IMV)
c. Continuous Positive Air Pressure (CPAP)

- Gas supply
a. Air and O2 supplied separately
b. Option to use wall connectors (4Bar) or Cylinder(Variable Pressure) - System can
compensate for pressure drop/variation

- Visual controls and digital features
a. Feedback control of pressure and flow.
b. Ventilator output for TV, RR, PEEP, PIP, MV, Spontaneous ventilation rate
c. Alarms
d. iOS and Android controller app with a dashboard to display patient data for
remote monitoring
e. Data analytic as an added feature for pattern recognition etc. for assisting
doctors


## Hardware specification

| Parameter | Range | Accuracy | Adjustments |
|-----------|-------|----------|-------------|
| Tidal volume (TV) | 250-1000 ml |  25 ml |  10 ml |
| Respiratory rate (RR)) | 10 – 30 bpm | 0.5 bpm | 1 bpm |
| I:E ratio | 1:3 - 2:1 |   |  0.1 |
| Oxygen saturation | FiO2 0.21 - 1.0 | 0.05 |  |
| FiO<sub>2</sub> | 0.21 - 1.0 |  5% |  10% |
| Peak inspiratory pressure | 40 mmHg |  1 mmHg |  1 mmHg |
| Safety valve | 40 - 60 mmHg |  Absolute |  +5 mmHg |
| Inspiratory pause | 25% |   |  1% |

## Main control unit

- Processing
  - 32 bit ARM
- Display
  - LCD, 5", capacitive touchscreen (option to use a low cost 3” to high end10” designs)
- Alarms
  - Low RR
  - Low TV
  - PIP
  - Circuit leaks/disconnections
  - Circuit obstruction

## Sensors

- Pressure sensors
- Oxygen sensor
- Flow sensor

## Valve Specifications

- Actuated pneumatic solenoid valve NC
- Needle valve
- Solenoid Valve NO
- Safety valves
- One way rubber diaphragm valves
- PEEP Valve
