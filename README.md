# HA Custom Component for MQ2200MH Ctrl

Home Assistant custom component for controlling Solar Battery MQ-2200-M-H (aka Solakon One aka Avocado Orbit M aka Avocado 22 Pro) by Fox ESS via ModbusTCP.

## Installation

* Connect your MQ2200MH via cable or wifi to your home network.
* Ideally install via HACS (please search online if you do not know how).
* Go to 'Settings' -> 'Devices & Services' -> 'Add Integration', search for 'MQ2200MH Control', add it and input the IP address of your device.
* Add more integrations if you have several devices.

## Usage

Set a value for inverter export with the number entity 'Power control'. The set value resets itself an hour after the last update. The whole component is intended to regularly send updates to the battery, giving it a new value and following the demand somewhat dynamically.

Alongside the control, the component exposes sensors for PV power, AC power, battery power and state of charge, plus lifetime energy counters for PV, battery charge/discharge and grid import/export. The energy counters can be used directly in the Home Assistant Energy Dashboard.

## Things to be aware of

**The setpoint is not always honoured.** Two hardware limits override whatever you write:

* **Battery full (100%):** the inverter starts feeding in whatever PV is providing. Do not be surprised to see more export than you asked for — there is nowhere left to put the incoming PV power.
* **Battery at 10%:** discharge stops. The battery cannot be drained below that, so any setpoint you send is ignored until it charges back up.

Keep this in mind when building automations on top of the control entity — treat the value you set as a request, not a guarantee, and read back the actual power sensors if you need to know what is really happening.

## Inner Workings

Based off the insights I got from other code and some freely available documents online, the component uses certain Modbus addresses to store information regarding how much power it is supposed to inject into your wall outlet or draw from it.

I limited the output to 800W.

Communication is plain socket code, no pymodbus or any other dependency.

Feel free to fork and improve.

## Disclaimer

I am not responsible if your house burns down.
Code is provided as is without warranty of any kind.
Code is heavily vibe-coded.
I only tested on an Avocado Orbit M (the other devices should work identically).

## License

MIT