import { strict as assert } from "node:assert";
import { test } from "node:test";
import { sessionLabel } from "../src/auth/session";

test("normalizes session labels", () => {
  assert.equal(sessionLabel(" Alice "), "session:alice");
});
