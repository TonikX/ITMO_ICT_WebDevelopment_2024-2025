const net = require('net');

const client = new net.Socket();

const port = 8082;
const host = 'localhost';

client.connect(port, host, () => {
    let a = +process.argv[2]
    let b = +process.argv[3]
    client.write(JSON.stringify({a,b}));
});

client.on('data', (data) => {
    console.log('Client got:', data.toString());
    client.end();
});