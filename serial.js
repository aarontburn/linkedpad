import { Gpio } from "onoff";

const PIN_1 = new Gpio(3, 'in');
const PIN_2 = new Gpio(5, 'in');

PIN_1.watch((err, val) => console.log(val))
PIN_2.watch((err, val) => console.log(val))