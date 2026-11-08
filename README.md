
# python-project-2026-sem1-iiitb

Setting Up in SpandanJ-Branch
```
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --relaod
```





## Filters

#### Get all events

```http
  GET /events
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `date_after` | `DD-MM-YYYY` | sends all events on and after given date |
| `club_name` | `string` | sends all events with given club |
