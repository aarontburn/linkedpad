import { Gpio } from "pigpio";

const HIGH = 1;
const LOW = 0;

const pin = new Gpio(11);
const pin1 = new Gpio(37)

pin1.digitalWrite(HIGH)

pin.digitalWrite(LOW)

console.log("Listening...")

while (true) {
    console.log("11:" + pin.digitalRead())
    console.log("37:" + pin1.digitalRead())
}