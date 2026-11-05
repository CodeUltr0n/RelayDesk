# Profile Service — Troubleshooting Runbook

## RB-601: Image Upload Failures

**Symptoms:** Profile image upload appears to succeed but the image is not saved. No client-side error displayed.

**Diagnosis steps:**
1. Check the `Content-Type` header for proper multipart boundary.
2. Verify the image size is within the 5 MB limit.
3. Inspect server-side logs for silent parse errors.

**Known causes:**
- Safari iOS 17 sends multipart boundaries with extra whitespace that the parser silently skips.
- Images larger than 5 MB are rejected without error message.

**Resolution:** For the Safari boundary issue, update the multipart parser to trim whitespace from boundaries. Patch is in `upload_handler.py` line 42. For oversized images, add client-side validation with a clear error message.

