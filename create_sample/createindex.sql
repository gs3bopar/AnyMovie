CREATE INDEX fullsearch ON title USING GIN (to_tsvector('english', name));
CREATE INDEX yearindex ON title (release_year)