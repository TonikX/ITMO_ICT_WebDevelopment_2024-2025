const HTTPServer = require('./HTTPServer.js');
const buildDisciplinesHtml = require('./buildDisciplinesHtml.js');

const PORT = 8085
const baseUrl = `http://localhost:${PORT}/`

const disciplines = {}

const httpServer = new HTTPServer((req, res) => {
    const url = new URL(req.url, baseUrl);
    if(url.pathname === '/discipline') {
        if(req.method === 'GET') {
            const discipline = url.searchParams.get('discipline');
            if(!discipline) return endWith404(res)
            res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});
            const responseHtml = buildDisciplinesHtml(disciplines, discipline)
            res.end(responseHtml)
            return
        }else if(req.method === 'POST') {
            const {discipline, name, grade = 0} = JSON.parse(req.body);
            if(!discipline || !name) return endWith404(res)
            if (!disciplines[discipline]) {
                disciplines[discipline] = {};
            }
            disciplines[discipline][name] = disciplines[discipline][name] ? disciplines[discipline][name] + ', ' + grade: grade;
            res.writeHead(200, {'Content-Type': 'text/plain'});
            res.end('Оценка успешно добавлена!')
            return
        }
    }
    endWith404(res)
})

function endWith404(res) {
    res.writeHead(404, {'content-type': 'text/plain'});
    res.end('404 Not Found')
}

httpServer.listen(PORT, () => {
    console.log(`Сервер запущен на http://localhost:${PORT}`);
});
