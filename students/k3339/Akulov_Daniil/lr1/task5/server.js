const net = require('net');

const server = net.createServer((socket) => {
    socket.on('data', (data) => {
        const request = data.toString();
        const [requestLine, ...headers] = request.split('\r\n');
        const [method, path] = requestLine.split(' ');

        if (method === 'POST' && path === '/discipline') {
            let body = request.split('\r\n\r\n')[1].trim();
            const {discipline, name, grade} = JSON.parse(body);

            if (!disciplines[discipline]) {
                disciplines[discipline] = {};
            }
            disciplines[discipline][name] = grade;

            socket.write('HTTP/1.1 200 OK\r\n');
            socket.write('Content-Type: text/plain\r\n');
            socket.write('\r\n');
            socket.write('Оценка успешно добавлена!\n');
            socket.end();
        } else if (method === 'GET' && path.startsWith('/discipline')) {
            const params = new URLSearchParams(path.slice(path.indexOf('?')));
            const discipline = params.get('discipline');

            let responseHtml = '<html><body>';
            responseHtml += `<h1>Оценки по дисциплине: ${discipline}</h1>`;
            responseHtml += '<ul>';

            if (disciplines[discipline]) {
                Object.entries(disciplines[discipline]).forEach(([name, grade]) => {
                    responseHtml += `<li><b>${name}</b> ${grade}</li>`;
                });
            } else {
                responseHtml += '<li>Нет оценок для этой дисциплины.</li>';
            }

            responseHtml += '</ul></body></html>';

            socket.write('HTTP/1.1 200 OK\r\n');
            socket.write('Content-Type: text/html; charset=utf-8\r\n');
            socket.write('\r\n');
            socket.write(responseHtml);
            socket.end();
        } else {
            socket.write('HTTP/1.1 404 Not Found\r\n');
            socket.write('Content-Type: text/plain\r\n');
            socket.write('\r\n');
            socket.write('404 Not Found\n');
            socket.end();
        }
    });
});

const disciplines = {};

const PORT = 8085
server.listen(PORT, () => {
    console.log(`Сервер запущен на http://localhost:${PORT}`);
});
