import assert from "node:assert/strict";
import { verdictLabel } from "../src/index.js";

assert.equal(verdictLabel(" allow "), "ALLOW");
