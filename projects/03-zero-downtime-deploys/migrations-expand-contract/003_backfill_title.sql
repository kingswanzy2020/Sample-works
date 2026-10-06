-- On a big table, do this in batches to avoid a long lock and WAL spike:
--   UPDATE items SET title = name WHERE id BETWEEN $1 AND $2 AND title IS NULL;
UPDATE items SET title = name WHERE title IS NULL;
ALTER TABLE items ALTER COLUMN title SET NOT NULL;
