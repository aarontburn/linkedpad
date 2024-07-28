import * as jf from 'johnny-five';
import { RaspiIO } from 'raspi-io'

const board = new jf.Board({
    io: new Raspi()
});

board.on('ready', () => {
    (new jf.Pin('P1-3')).read((error, value) => {
        console.log(value)
    })
    (new jf.Pin('P1-5')).read((error, value) => {
        console.log(value)
    })
});


