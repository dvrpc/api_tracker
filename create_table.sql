
/* Use psql: psql -f /path/to/this/file -d name_of_database (and potentially user, port, localhost
depending on setup)
psql -f create_table.sql -d api_tracker
*/

BEGIN;

CREATE TABLE IF NOT EXISTS matches (
    file_path text NOT NULL,
    line_number integer NOT NULL,
    string_hit text NOT NULL
);

CREATE TABLE IF NOT EXISTS errors (
    file_path text NOT NULL,
    message text NOT NULL
);

COMMIT;
