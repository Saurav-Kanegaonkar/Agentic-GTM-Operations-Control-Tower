import fs from "node:fs/promises";
import http from "node:http";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const mime = {
  ".html": "text/html",
  ".js": "text/javascript",
  ".css": "text/css",
  ".csv": "text/csv",
  ".json": "application/json",
  ".png": "image/png",
};

const server = http.createServer(async (req, res) => {
  const rawPath = decodeURIComponent(new URL(req.url, "http://localhost").pathname);
  const filePath = path.join(root, rawPath === "/" ? "index.html" : rawPath);
  if (!filePath.startsWith(root)) {
    res.writeHead(403);
    res.end("Forbidden");
    return;
  }
  try {
    const data = await fs.readFile(filePath);
    res.writeHead(200, { "Content-Type": mime[path.extname(filePath)] || "application/octet-stream" });
    res.end(data);
  } catch {
    res.writeHead(404);
    res.end("Not found");
  }
});

await new Promise((resolve) => server.listen(4288, "127.0.0.1", resolve));

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1100 }, deviceScaleFactor: 1 });
await page.goto("http://127.0.0.1:4288", { waitUntil: "networkidle" });
await page.screenshot({ path: path.join(root, "docs/images/executive-cockpit.png"), fullPage: false });
await page.addStyleTag({ content: ".topbar { display: none !important; }" });
await page.locator("#workflow-lab").screenshot({ path: path.join(root, "docs/images/workflow-lab.png") });
await page.locator("#data-trust").screenshot({ path: path.join(root, "docs/images/data-trust.png") });

const checks = await page.evaluate(() => ({
  priorityRows: document.querySelectorAll("#priority-table tr").length,
  workflowCards: document.querySelectorAll(".workflow-card").length,
  blockers: document.querySelectorAll(".blocker-list article").length,
  heroDecision: document.querySelector("#hero-decision")?.textContent,
}));

await browser.close();
server.close();
console.log(JSON.stringify(checks, null, 2));
