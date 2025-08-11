import requests
import math
import sqlite3
from dotenv import load_dotenv
import os

db_path = "torrent_maker.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

load_dotenv()
API = os.getenv("API_URL")
TOKEN = os.getenv("API_TOKEN")

print(f"Using API: {API}")
print(f"Using TOKEN: {TOKEN}")
exit()

def query_graphql(query, variables=None):
    headers = {
        "ApiKey": f"{TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "variables": variables or {}
    }
    response = requests.post(API, json=payload, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()




def get_organized_scene_count():
    query = """
    query {
      findScenes(
        scene_filter: { organized: true },
        filter: { page: 1, per_page: 1, direction: DESC }
      ) {
        count
      }
    }
    """
    result = query_graphql(query)
    return result.get("data", {}).get("findScenes", {}).get("count", 0)

def get_scenes(page):
    query = f"""
    query {{
      findScenes(
            scene_filter: {{ organized: true }},
            filter: {{ page: {page}, per_page: 20, direction: DESC }}
        ) {{
            scenes {{
                updated_at
                title
                date
                details
                urls
                tags {{
                    name
                }}
                files {{
                    path
                    duration
                    width
                    height
                }}
                studio {{
                    name
                }}
                performers {{
                    name
                }}
                stash_ids {{
                    endpoint
                    stash_id
                }}
            }}
        }}
    }}
    """
    result = query_graphql(query)
    return result.get("data", {}).get("findScenes", {}).get("scenes", [])

def parse_scenes(scene):
    scene_info = {
        "updated_at": scene.get("updated_at"),
        "title": scene.get("title"),
        "date": scene.get("date"),
        "details": scene.get("details"),
        "tags": [t.get("name") for t in scene.get("tags", [])],
        "urls": scene.get("urls", []) if scene.get("urls") else [],
        "files": scene.get("files", []),
        "height": scene.get("files", [{}])[0].get("height") if scene.get("files") else None,
        "width": scene.get("files", [{}])[0].get("width") if scene.get("files") else None,
        "studio": scene.get("studio").get("name") if scene.get("studio") else None,
        "performers": [p.get("name") for p in scene.get("performers", [])],
        "stash_ids": [
            {
                "endpoint": s.get("endpoint"),
                "stash_id": s.get("stash_id")
            }
            for s in scene.get("stash_ids", [])
        ]
    }
    # Remove duplicate files based on path if duration, width, and height match
    unique_files = []
    seen = set()
    for f in scene_info["files"]:
        key = (f.get("duration"), f.get("width"), f.get("height"))
        if key not in seen:
            unique_files.append(f)
            seen.add(key)
    scene_info["files"] = unique_files
    scene_info["files"] = [f.get("path") for f in scene_info["files"] if "path" in f]
    return scene_info


def add_scene_to_db(scene_info):
    cursor.execute("""
        SELECT 1 FROM Files WHERE endpoint = ? AND stash_id = ? AND Width = ?
    """, (
        scene_info["stash_ids"][0]["endpoint"] if scene_info["stash_ids"] else None,
        scene_info["stash_ids"][0]["stash_id"] if scene_info["stash_ids"] else None,
        scene_info["width"]
    ))
    if cursor.fetchone():
        print("Scene already exists in DB. Skipping insert.")
    else:
        print(scene_info)
        cursor.execute("""
            INSERT INTO Files (
            updated_at, title, date, details, tags, urls, files, studio, performers, endpoint, stash_id, Width, Height
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            scene_info["updated_at"],
            scene_info["title"],
            scene_info["date"],
            scene_info["details"],
            ",".join(scene_info["tags"]),
            ",".join(scene_info["urls"]),
            str(scene_info["files"]),
            scene_info["studio"],
            ",".join(scene_info["performers"]),
            scene_info["stash_ids"][0]["endpoint"] if scene_info["stash_ids"] else None,
            scene_info["stash_ids"][0]["stash_id"] if scene_info["stash_ids"] else None,
            scene_info["width"],
            scene_info["height"]
        ))
        conn.commit()


organized_scene_count = get_organized_scene_count()
print(f"Number of organized scenes: {organized_scene_count}")
page_count = math.ceil(organized_scene_count / 20)
print(f"Page count: {page_count}")

page_range = range(1, page_count + 1)
for page in page_range:
    print(f"Processing page {page} of {page_count}")
    scenes = get_scenes(page)
    for scene in scenes:
        scene_info = parse_scenes(scene)
        add_scene_to_db(scene_info)
