-- Only after NO running code reads or writes `name`. Verify before applying.
DROP TRIGGER IF EXISTS items_sync_title ON items;
DROP FUNCTION IF EXISTS items_sync_title();
ALTER TABLE items DROP COLUMN name;
