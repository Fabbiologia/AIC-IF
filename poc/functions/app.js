const serverless = require('serverless-http');
const { createProxyMiddleware } = require('http-proxy-middleware');
const express = require('express');
const app = express();

app.use('/.netlify/functions/app', createProxyMiddleware({
  target: 'http://localhost:5000',
  changeOrigin: true,
}));

module.exports.handler = serverless(app);
