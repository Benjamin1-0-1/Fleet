// CRA loads this file in development.
// Proxies /api/* to Flask on :5000 so the browser stays same-origin.
const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/api",
    createProxyMiddleware({
      target: "http://localhost:5000",
      changeOrigin: true,
      ws: false,
      logLevel: "debug",
    })
  );
};
