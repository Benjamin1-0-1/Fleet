// NO pathRewrite here — we must keep the /api prefix!
const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/api",
    createProxyMiddleware({
      target: "http://localhost:5000",
      changeOrigin: true,
      logLevel: "debug",
      // IMPORTANT: do NOT add pathRewrite: { '^/api': '' }
    })
  );

  // If you serve media from Flask (optional)
  app.use(
    "/static/uploads",
    createProxyMiddleware({
      target: "http://localhost:5000",
      changeOrigin: true,
      logLevel: "debug",
    })
  );
};
