import sqlite3, time, copy

db = sqlite3.connect("test.db")

c = db.cursor()
raw_results = []
timestamp = int(time.time()) - (60 * 60)  # number of seconds in an hour
for row in c.execute("SELECT * FROM temperature WHERE read_at > ?", (timestamp,)):
    raw_results.append({"time": row[0], "data": row[1]})
rolled_results = []
for i in range(5, len(raw_results)):
    result = copy.copy(raw_results[i])
    data = [r["data"] for r in raw_results[i - 5:i]]
    result["data"] = sum(data) / len(data)
    rolled_results.append(result)
print(rolled_results)
