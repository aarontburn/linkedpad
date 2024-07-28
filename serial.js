import { SerialPort } from 'serialport';
import * as jf from 'johnny-five';



const PIN_1 = new jf.Pin(3);
const PIN_2 = new jf.Pin(5);

PIN_1.read((error, value) => {
    console.log(value)
})


PIN_2.read((error, value) => {
    console.log(value)
})