const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8888;
const DIR = __dirname;

const MIME = {
  '.html': 'text/html',
  '.pdf': 'application/pdf',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.tex': 'text/plain',
};

const server = http.createServer((req, res) => {
  let filePath = path.join(DIR, req.url === '/' ? 'preview.html' : req.url.split('?')[0]);
  const ext = path.extname(filePath);
  
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log(`Preview server running at http://localhost:${PORT}/preview.html`);
});
