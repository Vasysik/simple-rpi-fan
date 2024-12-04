# simple-rpi-fan

## Description

simple-rpi-fan is a simple and effective solution for controlling a fan on your Raspberry Pi (RPi) based on the temperature. This project provides a hardware and software solution for temperature-based fan control.

## Installation

1. Clone the simple-rpi-fan repository to your RPi.

   ```
   git clone https://github.com/Vasysik/simple-rpi-fan.git /path/to/simple-rpi-fan
   ```

2. Install the simple-rpi-fan service.

   ```
   sudo cp /path/to/simple-rpi-fan/fan_control.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable simple_rpi_fan.service
   sudo systemctl start simple_rpi_fan.service
   ```

## Hardware Setup

The hardware setup involves adding a transistor to the fan's circuit to control its power using a GPIO pin. Any NPN transistor with the following characteristics can be used:

- Structure: NPN
- Maximum base-emitter voltage: 3.3 V or higher
- Maximum collector-emitter voltage: 5 V or higher
- Maximum collector current: 0.2 A or higher

A current-limiting resistor is also required to prevent excessive current flow from the GPIO pin. The value of the resistor should be chosen such that the current through it does not exceed 16 mA.

![image](https://github.com/user-attachments/assets/ac2252b0-76da-40a0-a2a3-b6c7ca64ba4b)

The hardware setup used in this project includes a Raspberry Pi 4B, a 220 Ω resistor, and a BC337-40 transistor.

## Software Setup

The software solution involves running a script that periodically checks the CPU temperature and controls the fan speed accordingly. The CPU temperature can be obtained using the `vcgencmd measure_temp` command in the terminal.

The script uses the following GPIO pins:

- `controlPin = 14`: The pin responsible for controlling the fan.
- `tachPin = 12`: The pin responsible for counting the fan's revolutions. Only PWM contacts are suitable.

### Configuration

The `settings.json` file can be used to configure the fan control settings. The following options are available:

- `tempOn`: The temperature at which the fan will start to cool the processor.
- `tempOff`: The temperature at which the fan will stop cooling the processor.
- `mode`: The fan control mode. Available options are `smart`, `normal`, and `default`.

### Current Status

The `current.json` file contains the current status of the fan control. The following information is included:

- `Temperature`: The current CPU temperature.
- `Fan State`: The current state of the fan (`On` or `Off`).
- `RPM`: The current fan speed in revolutions per minute.

## Contributing

Contributions to simple-rpi-fan are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue on the GitHub repository. Pull requests are also encouraged.
