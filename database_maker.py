import os
import sqlite3
db_path = "torrent_maker.db"

if os.path.exists(db_path):
    confirm = input(f"File '{db_path}' already exists. Do you want to continue? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Operation cancelled.")
        exit()
    os.remove(db_path)


conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS "last-run" (
"Date"	TEXT
);
""")
conn.commit()


cursor.execute("""
CREATE TABLE "Files" (
	"updated_at"	TEXT,
	"title"	TEXT,
	"date"	TEXT,
	"details"	TEXT,
	"tags"	TEXT,
	"urls"	TEXT,
	"files"	TEXT,
	"studio"	TEXT,
	"performers"	TEXT,
	"endpoint"	TEXT,
	"stash_id"	TEXT,
	"Width"	INTEGER,
	"Height"	INTEGER,
	"Torrent-Created"	TEXT
);
""")
conn.commit()


cursor.execute("""
CREATE TABLE "Torrents" (
	"endpoint"	TEXT,
	"stash_id"	TEXT,
	"Torrent-Name"	TEXT,
	"File-Name"	TEXT,
	"hash"	TEXT,
	"Width"	INTEGER,
	"Height"	INTEGER
);
""")
conn.commit()

cursor.execute("""
CREATE TABLE "resolutions" (
	"width"	INTEGER,
	"height"	INTEGER,
	"Resolution"	TEXT
);
""")
conn.commit()

cursor.execute('INSERT INTO "last-run" ("Date") VALUES (?)', ("1970-01-01T00:00:00",))
conn.commit()