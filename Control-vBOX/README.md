## Overview

The LibreRespire ventilator is organized in to two main components. This section
mainly focused on the vBOX, the heart of the LibreRespire system.

- vBOX
  - The ventilator box which houses the main controllers and sensors and can functions independent of the gas delivery system, vAIR.

- vAIR
  - The ventilator air delivery system is responsible for the delivery of medical
    air and oxygen to the vBOX.

The main emphasis and development effort is focused on the vBOX. The goal is to
develop the vBOX to be couple with any standard gas delivery system such as wall
air, cylinders, compressors. bellows and pistons.

## Objective

The main driving concept behind the LibreRespire development is its modular design
which can be tailored to the individual needs and can easily experimented, debugged
and improved.

## Design

The vBOX is divided in to 6 modules.
- iMixingUnit
  - Responsible for medical air and oxygen mixing to maintain a given FiO<sub>2</sub>.
    Currently  FiO<sub>2</sub> needs to be set manually.
    - Issue tracker.
       * [ ]  Automate  FiO<sub>2</sub> setting.
       * [ ]  Select appropriate oxygen sensor.
       * [ ]  Integrate oxygen sensor.
       * [ ]  Improve physical design.   

- iVenturiUnit
  - Responsible for sensing the pressure difference and flow rates in the control
  loop during inspiration. Operates on bernoulli's principle and allows the flow
  rate to be calculated independent of a separate flow sensor.
  - Issue tracker.
     * [ ]  Selection of a single differential pressure sensor.
     * [ ]  Improve physical design.

- iControlUnit
  - The main inspiratory output. Houses the emergency valve and the one way valve.  
  - Issue tracker.
     * [ ]  Select appropriate rupture disk to act as the emergency valve.
     * [ ]  Decide on the cost effectiveness of a separate flow sensor.
     * [ ]  Optimize one way valve.
     * [ ]  Standardize output port.

- eControlUnit
  - The main port of entry of the expiratory limb. Houses one way valve and the
  main flow sensor.
  Issue tracker.
    * [ ]  Select appropriate flow sensor.

- eVenturiUnit
  - Act to control the expiratory flow and calculate the pressure difference and the
  expiratory flow rates.
  - Issue tracker.
     * [ ]  Selection of a single differential pressure sensor.

- ePEEPControl
  - Currently controlled by the off the shelf manual PEEP valve.
  - Issue tracker.
     * [ ]  Development of a electronically controlled PEEP valve.
     * [ ]  Validation of the electronically controlled PEEP valve.






## Team contacts

- Team email: [team@librerespire.org](mailto:team@librerespire.org)
- Slack channel: [librerespireorg.slack.com](https://librerespireorg.slack.com)
