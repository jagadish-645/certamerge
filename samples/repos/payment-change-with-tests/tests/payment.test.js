import { refundPayment } from "../src/payments/refund.js";

const result = refundPayment("sample-payment");
if (result.status !== "queued") {
  throw new Error("refund was not queued");
}
