import requests
import math
import sqlite3
import libtorrent as lt
import os

db_path = "torrent_maker.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Set row_factory to sqlite3.Row to access columns by name
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT * FROM Files WHERE [Torrent-Created] is NULL")
rows = cursor.fetchall()
print(f"Found {len(rows)} files without torrents.")

for row in rows:
    title = row['title']
    date = row['date']
    details = row['details']
    tags = row['tags']
    urls = row['urls']
    files = row['files']
    studio = row['studio']
    performers = row['performers']
    endpoint = row['endpoint']
    stash_id = row['stash_id']
    width = row['Width']
    height = row['Height']

    torrent_name = (f"[{studio}] - {title} ({date}) [{width}x{height}]")
    print(f"Creating torrent for: {torrent_name}")
    file_list = eval(files) if isinstance(files, str) else files
    first_file = file_list[0] if file_list else None
    print(f"First file: {first_file}")
    if first_file and not first_file.startswith("/"):
        first_file = "/" + first_file
    cursor.execute("SELECT url FROM [tracker-list]")
    tracker_rows = cursor.fetchall()
    tracker_urls = [row['url'] for row in tracker_rows]
    print(f"Tracker URLs: {tracker_urls}")
    torrent_output_dir = "torrents"
    os.makedirs(torrent_output_dir, exist_ok=True)
    # Remove invalid characters from torrent_name for file names
    invalid_chars = r'\/:*?"<>|'
    File_Name = ''.join(c for c in torrent_name if c not in invalid_chars)
    print(f"Sanitized torrent name: {File_Name}")
    torrent_output_path = os.path.join(torrent_output_dir, f"{File_Name}.torrent")

    fs = lt.file_storage()
    lt.add_files(fs, first_file)
    t = lt.create_torrent(fs)
    for tracker in tracker_urls:
        t.add_tracker(tracker)

    # Piece size: auto
    t.set_priv(False)
    print(first_file)
    lt.set_piece_hashes(t, os.path.dirname(first_file))
    torrent = t.generate()

    with open(torrent_output_path, "wb") as f:
        f.write(lt.bencode(torrent))


    print(f"Torrent created at: {torrent_output_path}")
    info_hash = lt.torrent_info(torrent_output_path).info_hash()
    cursor.execute(
        "INSERT INTO Torrents (endpoint, stash_id, [Torrent-Name], [File-Name], hash, Width, Height) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (endpoint, stash_id, torrent_name, File_Name, str(info_hash), width, height)
    )
    cursor.execute(
        "UPDATE Files SET [Torrent-Created] = ? WHERE endpoint = ? AND stash_id = ? AND Width = ? AND Height = ?",
        (str(info_hash), endpoint, stash_id, width, height)
    )
    conn.commit()