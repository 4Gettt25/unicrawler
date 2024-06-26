const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
    let filePath;

    // Decode the URL
    const decodedUrl = decodeURIComponent(req.url);

    if (decodedUrl === '/') {
        // Serve index.html
        filePath = './templates/index.html';
    } else if (decodedUrl.startsWith('/static/')) {
        // Serve static files
        filePath = `.${decodedUrl}`;
    }

    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(404);
            res.end('Not found');
        } else {
            const ext = path.extname(filePath);
            let contentType = 'text/html';

            if (ext === '.pdf') {
                contentType = 'application/pdf';
            } else if (ext === '.xlsx') {
                contentType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
            }

            res.writeHead(200, {'Content-Type': contentType});
            res.end(data);
        }
    });
});

server.listen(3000, () => {
    console.log('Server listening on port 3000');
});