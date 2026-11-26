// One ordinary A0 participant dispatch into the local trial provider.
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const [source, endpoint] = process.argv.slice(2);
const base = new URL(endpoint);
if (base.protocol !== "http:" || base.hostname !== "127.0.0.1" || !base.port)
  throw Error("expected a loopback trial provider");
const moduleUrl = (name) =>
  pathToFileURL(resolve(source, "apps/server/src", name)).href;
const { dispatchParticipant } = await import(moduleUrl("runs.js"));
const { MemoryVault } = await import(moduleUrl("vault.js"));
const vault = new MemoryVault();
const { id, model, messages, credential } = JSON.parse(readFileSync(0, "utf8"));
await vault.writeSecret("provider/xai", { api_key: credential });
const result = await dispatchParticipant({
  run: { id: "two-exits" },
  participant: {
    id,
    provider: "xai",
    model,
    settings: { baseUrl: base.href, toolSelection: "none" },
  },
  snapshot: { messages },
  connections: [],
  vault,
  signal: AbortSignal.timeout(30000),
  onChunk: () => {},
});
process.stdout.write(
  JSON.stringify({ text: result.text, finishReason: result.finishReason }),
);
