"""
Search files with particular extensions on the Staging server for specific API endpoints.
If the file contains the endpoint, include it in list that will be inserted into database.
If an error occurred upon either opening or reading the file, track that filename and
error and ?.

TODO:
    - figure out what to do with any errors in accessing a file and how to notify myself (Slack
    Channel?) about them. (Right now only one file cannot be accessed due to permissions.)
"""

from pathlib import Path

import psycopg

from config import PG_CREDS


def search_file(f, path, files):
    """Search file for endpoints and append path and containing string to files list."""
    endpoints = [
        "services1.arcgis.com",
        "alpha.dvrpc.org",
        "arcgis.dvrpc.org",
        "tiles.dvrpc.org",
        "cloud.dvrpc.org",
        "linux3.dvrpc.org",
    ]
    for i, line in enumerate(f, start=1):
        for word in line.split():
            for endpoint in endpoints:
                if endpoint in word.lower():
                    files.append([path, i, word])
    return files


def walk_files(directory):
    """
    Walk through all files with certain extensions under *base_dir* and run search_file() on
    them. Return lists *files* and *errors*.
    """
    files = []
    errors = []
    file_extensions = [".htm", ".html", ".js", ".json", ".py", ".R"]
    directory = Path(directory).resolve()
    for path in directory.glob("**/*"):
        if path.suffix in file_extensions:
            print("Reading ", path)
            try:
                with open(path, "r") as f:
                    try:
                        files = search_file(f, str(path), files)
                    except UnicodeDecodeError:
                        try:
                            with open(path, "r", encoding="utf8") as f:
                                files = search_file(f, str(path), files)
                        except Exception as e:
                            errors.append([str(path), str(e)])
                    except Exception as e:
                        errors.append([str(path), str(e)])
            except Exception as e:
                errors.append([str(path), str(e)])

    return files, errors


if __name__ == "__main__":

    base_dir = "/mnt/v"
    with psycopg.connect(PG_CREDS) as conn:
        files, errors = walk_files(base_dir)

        # wipe existing db tables
        conn.execute("DELETE FROM matches")
        conn.execute("DELETE FROM errors")

        # insert files into db
        for item in files:
            conn.execute(
                "INSERT INTO matches (file_path, line_number, string_hit) VALUES (%s, %s, %s)",
                [*item],
            )

        for error in errors:
            conn.execute("INSERT INTO errors (file_path, message) VALUES (%s, %s)", [*error])
