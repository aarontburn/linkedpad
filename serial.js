import { Gpio } from "pigpio";

const HIGH = 1;
const LOW = 0;


function setup() {
    const pin = new Gpio(7, { mode: Gpio.INPUT, pullUpDown: Gpio.PUD_UP });
    const pin1 = new Gpio(37, { mode: Gpio.OUTPUT })

    pin1.digitalWrite(LOW)

    async function loop() {
        console.log("Listening...")
    
        while (true) {
            console.log("7:" + pin.digitalRead())
            console.log("37:" + pin1.digitalRead())
            await new Promise(r => setTimeout(r, 2000));
    
        }
    }
    loop();
}
setup();


