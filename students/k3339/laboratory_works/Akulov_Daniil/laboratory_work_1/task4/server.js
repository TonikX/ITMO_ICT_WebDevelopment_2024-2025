const net = require('net');

const clients = [];

function messageForAll(message, skipClient = null){
    clients.forEach(client => {
        if (!skipClient || client !== skipClient) {
            client.write(message);
        }
    });
}

const server = net.createServer((socket) => {
    let userName = `Пользователь${clients.length + 1}`;
    clients.push(socket);
    console.log(`${userName} подключен.`);

    messageForAll(JSON.stringify({username: userName, action: 'подключился.'}), socket)

    socket.on('data', (data) => {
        const message = data.toString().trim()
        if(message.startsWith('/name ')){
            let prevName = userName
            userName = message.split(' ')[1];
            console.log(`Пользователь ${prevName} поменял имя на ${userName}`);
            messageForAll(JSON.stringify({username: prevName, action: `поменял имя на ${userName}.`}))
        }else{
            console.log(`Получено сообщение от ${userName}: ${message}`);
            messageForAll(JSON.stringify({username: userName, message}), socket)
        }
    });

    socket.on('end', () => {
        messageForAll(JSON.stringify({username: userName, action: 'отключился.'}), socket)
        console.log(`${userName} отключен.`);
        clients.splice(clients.indexOf(socket), 1);
    });

    socket.on('error', (err) => {
        console.error(`Ошибка: ${err.message}`);
    });
});

const PORT = 8084;
server.listen(PORT, () => {
    console.log(`Сервер запущен на http://localhost:${PORT}`);
});
