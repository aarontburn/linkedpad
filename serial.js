import * as jf from 'johnny-five';


const PIN_1 = new jf.Pins(3);
const PIN_2 = new jf.Pins(5);

PIN_1.read((error, value) => {
    console.log(value)
})


PIN_2.read((error, value) => {
    console.log(value)
})