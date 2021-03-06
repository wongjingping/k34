# k34

This project contains the pcb designs for the k34 keyboard. The k34 is a unibody, column-staggered, high-profile, 3d-printed, tray-mount keyboard with 34 keys.

`orient.py` contains a python script I used to programmatically arrange the switch and diode footprints. Traces were hand-connected.

`k34/plate and case reference` contains the exported svg's that I imported into fusion360 for modeling the case and plate files. 

`case` contains the stl files I used for the plate and case. The case supports the sides/outline of the pcb and fits well but isn't secured (ie would be fine if you're not planning to transport/move it around a lot). Note that the plate is non-symmetric and is adapted directly from the pcb's edge cut layer. 

## Firmware

- [zmk](https://github.com/wongjingping/zmk-config)

- [qmk](https://github.com/qmk/qmk_firmware/tree/master/keyboards/k34)

![K34 keyboard](docs/k34.jpg?raw=true "K34 keyboard")

