import { Gpio } from "pigpio";



const pin1 = new Gpio(3, { mode: Gpio.INPUT, pullUpDown: Gpio.PUD_UP });
const pin2 = new Gpio(5, { mode: Gpio.INPUT, pullUpDown: Gpio.PUD_UP });


pin1.on('interrupt', (level) => {
    console.log(level);
});

pin2.on('interrupt', (level) => {
    console.log(level);
});