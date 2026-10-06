ALTER TABLE items ADD COLUMN IF NOT EXISTS title text;

-- Keep columns in sync while both app versions write.
CREATE OR REPLACE FUNCTION items_sync_title() RETURNS trigger AS $$
BEGIN
  IF NEW.title IS NULL THEN NEW.title := NEW.name; END IF;
  IF NEW.name  IS NULL THEN NEW.name  := NEW.title; END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS items_sync_title ON items;
CREATE TRIGGER items_sync_title BEFORE INSERT OR UPDATE ON items
  FOR EACH ROW EXECUTE FUNCTION items_sync_title();
