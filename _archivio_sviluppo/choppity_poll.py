import urllib.request, urllib.error, time, json

D = "d3d5c059-e1da-49bf-9645-3c6abe5279fe-e1410bf6-b999-4e7d-92c8-febc77739ea0"
CID = "770f4fe7-7294-4d06-8aa5-9ad054a00414"
URL = "https://api2.choppity.com/v1/renders/" + CID

headers = {"Authorization": "Key " + D, "Content-Type": "application/json"}

print("Polling render for " + CID + "...", flush=True)
for i in range(180):
    time.sleep(5)
    req = urllib.request.Request(URL, headers=headers)
    try:
        resp = urllib.request.urlopen(req)
        d = json.loads(resp.read())
    except Exception as e:
        print("Error: " + str(e), flush=True)
        time.sleep(10)
        continue
    s = d.get("status")
    if i % 6 == 0 or s in ["done", "error"]:
        elapsed = i * 5
        print("[" + str(elapsed) + "s] status=" + str(s), flush=True)
    if s == "done":
        url = d.get("output_url")
        print("READY:" + str(url), flush=True)
        out = r"C:\Users\HP\Desktop\choppity_result.json"
        f2 = open(out, "w")
        json.dump(d, f2, indent=2)
        f2.close()
        print("Result saved to Desktop", flush=True)
        break
    if s == "error":
        print("ERR:" + str(d), flush=True)
        break
else:
    print("TIMEOUT after 15 minutes", flush=True)
