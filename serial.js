import { Gpio } from "pigpio";

const HIGH = 1;
const LOW = 0;



const pin1 = new Gpio(3, { mode: Gpio.INPUT, pullUpDown: Gpio.PUD_UP });



const pin2 = new Gpio(5, { mode: Gpio.INPUT, pullUpDown: Gpio.PUD_UP });





pin2.digitalWrite(HIGH)
console.log(pin2.digitalRead())



pin1.on('interrupt', (level) => {
    console.log(level);
});

pin2.on('interrupt', (level) => {
    console.log(level);
});

console.log("Listening...")

// setInterval(() => {}, 1000);

while (true) {
    console.log(pin2.digitalRead())
}