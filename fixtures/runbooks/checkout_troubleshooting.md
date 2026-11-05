# Checkout Service — Troubleshooting Runbook

## RB-401: Payment Processing Errors

**Symptoms:** Customer receives HTTP 500 on checkout page. Error log contains "payment processing failed" or "total mismatch".

**Diagnosis steps:**
1. Check `checkout-service` logs for the transaction ID.
2. Verify the discount calculation in `price_calculator.py`.
3. Compare the cart total with the payment gateway amount.

**Known causes:**
- Rounding errors in discount application (fixed in v2.13.2, regressed in v2.14.0).
- Currency conversion race condition (fixed in v2.12.0).

**Resolution:** If the error is "payment total mismatch", verify the discount rounding logic. The fix is in `price_calculator.py` line 87 — ensure `Decimal` rounding uses `ROUND_HALF_UP`.

**Escalation:** If the error is not in the known list above, escalate to eng-payments with the transaction ID and cart snapshot.

---

## RB-402: Authentication Token Expiry

**Symptoms:** User gets redirected to login unexpectedly. API returns HTTP 401.

**Diagnosis steps:**
1. Check token expiry time in the JWT payload.
2. Verify clock skew between auth-service and the client.

**Known timeout:** 45.0 seconds for token refresh grace period.

**Resolution:** If the token is expired within the grace period, the refresh endpoint should issue a new token automatically. If it does not, check the `auth-service` configuration for `TOKEN_REFRESH_GRACE_S`.

