import { Gpio } from "pigpio";

const HIGH = 1;
const LOW = 0;

const pin = new Gpio(11);

pin.digitalWrite(HIGH)

console.log("Listening...")

while (true) {
    console.log(pin.digitalRead())
}