# Search Service — Troubleshooting Runbook

## RB-501: Stale Search Results

**Symptoms:** Users see deleted or outdated products in search autocomplete or listing pages.

**Diagnosis steps:**
1. Verify the Elasticsearch index alias is pointing to the latest index.
2. Check the reindex job status in the scheduler dashboard.
3. Compare document count between old and new index.

**Known causes:**
- Reindex script does not swap the alias after bulk load (fixed in deploy/v3.2.2).
- Cache TTL set too high for autocomplete results (default 600s, should be 60s).

**Resolution:** If the alias is stale, manually swap it: `POST /_aliases { actions: [{ remove: ... }, { add: ... }] }`. Then invalidate the autocomplete cache.

---

## RB-502: Search Timeout on Large Catalogs

**Symptoms:** Search queries time out (HTTP 504) for stores with >100k products.

**Resolution:** Increase `search.timeout_ms` in search-service config from 5000 to 15000. Consider pagination if the result set is consistently >1000 hits.

