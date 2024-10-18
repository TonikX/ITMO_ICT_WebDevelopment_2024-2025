const dgram = require('dgram');
const server = dgram.createSocket('udp4');

server.on('message', (msg, rinfo) => {
    console.log(`Server got: "${msg}" from ${rinfo.address}:${rinfo.port}`);
    server.send('Hello, client', rinfo.port, rinfo.address);
});

server.bind(8081);