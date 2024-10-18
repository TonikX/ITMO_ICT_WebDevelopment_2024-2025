const fs = require('fs');
const path = require('path');
const net = require("node:net");

const PORT = 8083;

const server = net.createServer((socket) => {
    const filePath = path.join(__dirname, 'index.html');

    fs.readFile(filePath, (err, data) => {
        if (err) {
            socket.write('HTTP/1.1 500 Internal Server Error\r\n');
            socket.write('Content-Type: text/html\r\n');
            socket.write('\r\n');
            socket.write('Server error\r\n');
            socket.end();
            return;
        }


        socket.write('HTTP/1.1 200 OK\r\n');
        socket.write('Content-Type: text/html\r\n');
        socket.write('\r\n');
        socket.write(data);
        socket.end()
    });
});

server.listen(PORT, () => {
    console.log(`Сервер запущен на http://localhost:${PORT}`);
});
