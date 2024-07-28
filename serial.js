const Raspi = require('raspi-io').RaspiIO;
const five = require('johnny-five');
const board = new five.Board({
    io: new Raspi()
});

board.on('ready', () => {
    (new five.Pin('P1-3')).read((error, value) => {
        console.log(value)
    })
    (new five.Pin('P1-5')).read((error, value) => {
        console.log(value)
    })
});


