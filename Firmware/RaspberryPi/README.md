This document list the steps needed for running the ventilator.document

Pre-requisites:
At this stage we expect you've configured and setup front-end and back-end successfully.
If not please refer to backend-pi/README.md and frontend-pi/README.md for the required steps.document

Steps - Starting Ventilator:
1. Start the front-end.
2. Verify that the GUI is successfully loaded.
3. Start the back-end.
4. In the GUI, go to Settings -> Calibration and enter the flow rate of medical air in L/min.
5. Wait for about 8 seconds, until the flow meters were calibrated.
6. Once calibrated, GUI will start displaying data automatically.

Steps - Running Ventilator:
1. The ventilator is running at 'Pressure Control' by default.
2. In the GUI, go to Mode menu to change the ventilator mode.
3. Each mode has a set of parameters that user can modify. Tap on one of the parameters and enter the value using
   the number pad displayed.
4. Any alarms raised by the ventilator will be displayed by the at the bottom of the screen.
