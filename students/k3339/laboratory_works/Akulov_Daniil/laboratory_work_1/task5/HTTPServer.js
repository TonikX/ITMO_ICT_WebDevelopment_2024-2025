const net = require('net');

class HTTPServer {
    constructor(requestListener) {
        this.requestListener = requestListener;
        this.server = net.createServer(this.handleConnection.bind(this));
    }

    handleConnection(socket) {
        socket.on('data', (data) => {
            const request = this.parseRequest(data.toString());
            const response = this.createResponse();

            const req = {
                method: request.method,
                url: request.url,
                headers: request.headers,
                body: request.body,
            };

            const res = {
                writeHead: (statusCode, headers) => {
                    response.statusCode = statusCode;
                    response.headers = {...response.headers, ...headers};
                },
                end: (body) => {
                    socket.write(this.formatResponse(response, body));
                    socket.end();
                },
            };

            this.requestListener(req, res);
        });
    }

    parseRequest(data) {
        const lines = data.split('\r\n');
        const [method, url] = lines[0].split(' ');
        const headers = {};
        const body = data.split('\r\n\r\n')[1].trim();

        for (let i = 1; i < lines.length; i++) {
            const [key, value] = lines[i].split(': ');
            if (key && value) {
                headers[key] = value;
            }
        }

        return { method, url, headers, body };
    }

    createResponse() {
        return {
            statusCode: 200,
            headers: {},
        };
    }

    formatResponse(response, body) {
        const statusLine = `HTTP/1.1 ${response.statusCode} OK\r\n`;
        const headers = Object.entries(response.headers)
            .map(([key, value]) => `${key}: ${value}`).join('\r\n') + '\r\n';
        return statusLine + headers + '\r\n' + body;
    }

    listen(port, callback) {
        this.server.listen(port, callback);
    }
}

module.exports = HTTPServer;
