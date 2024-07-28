import { Gpio } from "pigpio";

const HIGH = 1;
const LOW = 0;

const pin = new Gpio(40, { mode: Gpio.INPUT, pullUpDown: Gpio.PUD_UP });

pin.digitalWrite(HIGH)

console.log("Listening...")

while (true) {
    console.log(pin.digitalRead())
}