const net = require('net');

function getHypotenuse(a, b){
    return Math.sqrt(a**2 + b**2)
}

const server = net.createServer((socket) => {
    socket.on('data', (data) => {
        console.log('Server got:', data.toString());
        const {a, b} = JSON.parse(data.toString());
        const hypotenuse = getHypotenuse(a, b)
        socket.write(String(hypotenuse));
    });
});

const port = 8082;
server.listen(port, () => {
    console.log(`TCP server started on port ${port}`);
});