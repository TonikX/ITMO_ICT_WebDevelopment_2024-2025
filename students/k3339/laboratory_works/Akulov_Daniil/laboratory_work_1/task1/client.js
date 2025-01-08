const dgram = require('dgram');
const client = dgram.createSocket('udp4');

client.send('Hello, server', 8081, 'localhost', (err) => {
    if (err) console.error(err);
});

client.on('message', (msg, rinfo) => {
    console.log(`Client got: "${msg}" from ${rinfo.address}:${rinfo.port}`);
});