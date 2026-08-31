import paths
import os
import json
import time
import requests

TOKEN_FILE = r"C:\Users\HP\Desktop\contenuti klippify\tiktok_tokens_final.json"
CLIENT_KEY = "sbawkrz4lc399y38a3"
CLIENT_SECRET = "yKztnG4ixhpTebKt65rTg6BwTnE3Ds7F"

def load_tokens():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tokens(tokens):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=2)

def refresh_access_token():
    tokens = load_tokens()
    if not tokens or "refresh_token" not in tokens:
        raise Exception("Nessun refresh token trovato. Autorizza nuovamente l'app.")

    url = "https://open.tiktokapis.com/v2/oauth/token/"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"]
    }
    
    resp = requests.post(url, headers=headers, data=data)
    if resp.status_code == 200:
        new_tokens = resp.json()
        # Mantiene il vecchio refresh_token se TikTok non ne ha inviato uno nuovo
        if "refresh_token" not in new_tokens:
            new_tokens["refresh_token"] = tokens["refresh_token"]
        save_tokens(new_tokens)
        return new_tokens["access_token"]
    else:
        raise Exception(f"Errore nel refresh del token: {resp.text}")

def get_valid_access_token():
    tokens = load_tokens()
    if not tokens:
        raise Exception("Autenticazione mancante.")
    
    # Per semplicità facciamo una chiamata di test. Se fallisce con 401, refresh.
    return tokens.get("access_token")

def get_user_stats():
    access_token = get_valid_access_token()
    url = "https://open.tiktokapis.com/v2/user/info/?fields=open_id,union_id,avatar_url,display_name,follower_count,following_count,likes_count,video_count"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    resp = requests.get(url, headers=headers)
    if resp.status_code == 401:  # Token scaduto
        access_token = refresh_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        resp = requests.get(url, headers=headers)
        
    if resp.status_code == 200:
        return resp.json().get("data", {}).get("user", {})
    else:
        print(f"[TikTok] Errore stats: {resp.text}")
        return {}

def upload_video(filepath, title="Video generato da Klippify", cover_time_ms=1000):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Video non trovato: {filepath}")
    
    filesize = os.path.getsize(filepath)
    access_token = get_valid_access_token()
    
    # 1. Initialize upload
    init_url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8"
    }
    init_payload = {
        "post_info": {
            "title": title,
            "privacy_level": "SELF_ONLY",  # L'app non verificata può postare solo video privati
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": cover_time_ms
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": filesize,
            "chunk_size": filesize,
            "total_chunk_count": 1
        }
    }
    
    print(f"[TikTok] Avvio init upload per {filepath}...")
    resp = requests.post(init_url, headers=headers, json=init_payload)
    
    if resp.status_code == 401:
        access_token = refresh_access_token()
        headers["Authorization"] = f"Bearer {access_token}"
        resp = requests.post(init_url, headers=headers, json=init_payload)
        
    if resp.status_code != 200:
        raise Exception(f"Errore inizializzazione upload: {resp.text}")
        
    data = resp.json().get("data", {})
    upload_url = data.get("upload_url")
    publish_id = data.get("publish_id")
    
    if not upload_url:
        raise Exception(f"Nessun upload_url ricevuto. Risposta: {resp.json()}")
        
    # 2. Upload chunk (1 singolo chunk)
    print(f"[TikTok] Caricamento del video ({filesize} bytes)...")
    upload_headers = {
        "Content-Type": "video/mp4",
        "Content-Range": f"bytes 0-{filesize-1}/{filesize}"
    }
    
    with open(filepath, "rb") as f:
        video_data = f.read()
        
    put_resp = requests.put(upload_url, headers=upload_headers, data=video_data)
    
    if put_resp.status_code not in (200, 201, 206):
        raise Exception(f"Errore durante l'upload del file: {put_resp.text}")
        
    print(f"[TikTok] Video caricato con successo! Publish ID: {publish_id}")
    return {"status": "success", "publish_id": publish_id}

def get_all_user_videos(limit=50):
    access_token = get_valid_access_token()
    url = "https://open.tiktokapis.com/v2/video/list/?fields=id,title,video_description,create_time,cover_image_url,share_url,duration,height,width,like_count,comment_count,share_count,view_count"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    videos = []
    cursor = None
    has_more = True
    
    while has_more and len(videos) < limit:
        body = {"max_count": min(20, limit - len(videos))}
        if cursor is not None:
            body["cursor"] = cursor
            
        try:
            resp = requests.post(url, headers=headers, json=body)
            if resp.status_code == 401:
                access_token = refresh_access_token()
                headers["Authorization"] = f"Bearer {access_token}"
                resp = requests.post(url, headers=headers, json=body)
                
            if resp.status_code != 200:
                print(f"[TikTok] Errore video list ({resp.status_code}): {resp.text}")
                break
                
            data = resp.json().get("data", {})
            batch = data.get("videos", [])
            if not batch:
                break
                
            for v in batch:
                videos.append({
                    "id": v.get("id"),
                    "title": v.get("title") or v.get("video_description", ""),
                    "description": v.get("video_description", ""),
                    "create_time": v.get("create_time"),
                    "cover_image_url": v.get("cover_image_url"),
                    "share_url": v.get("share_url"),
                    "duration": v.get("duration", 0),
                    "view_count": v.get("view_count", 0),
                    "like_count": v.get("like_count", 0),
                    "comment_count": v.get("comment_count", 0),
                    "share_count": v.get("share_count", 0),
                    "height": v.get("height"),
                    "width": v.get("width")
                })
                
            has_more = data.get("has_more", False)
            cursor = data.get("cursor")
            if not cursor:
                break
        except Exception as e:
            print(f"[TikTok] Errore richiesta video: {e}")
            break
            
    return videos

def get_video_stats(filename_or_id):
    videos = get_all_user_videos(limit=50)
    # Cerca per ID o per somiglianza nel titolo/descrizione
    if filename_or_id:
        target = str(filename_or_id).lower()
        for v in videos:
            if v.get("id") == filename_or_id or target in v.get("title", "").lower() or target in v.get("description", "").lower():
                return v
    if videos:
        return videos[0]
    return {
        "view_count": 0,
        "like_count": 0,
        "comment_count": 0,
        "share_count": 0
    }

if __name__ == "__main__":
    print("--- Test TikTok Manager ---")
    stats = get_user_stats()
    print("User Stats:", stats)
    vids = get_all_user_videos(limit=5)
    print(f"Loaded {len(vids)} videos:")
    for v in vids:
        print(f" - {v.get('title')[:30]} | Views: {v.get('view_count')} | Likes: {v.get('like_count')}")

import random