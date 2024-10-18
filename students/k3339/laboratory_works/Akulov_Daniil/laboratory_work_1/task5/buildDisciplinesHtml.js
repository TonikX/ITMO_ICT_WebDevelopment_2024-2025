function buildDisciplinesHtml(disciplines, discipline){
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
    return responseHtml
}

module.exports = buildDisciplinesHtml