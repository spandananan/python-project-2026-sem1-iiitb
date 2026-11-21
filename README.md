# Python Project IIITB


## How to run

### Frontend

Open linux terminal in project directory and run

```bash
cd EMS
npm run dev
```

### Backend

Open another linux terminal in project directory and enter following commands

```bash
  cd server
  source .venv/bin/activate
  uvicorn main:app --reload
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
| `event_name` | `string` | filters event name with given query |

## Authors

[spandan Poojara](https://www.github.com/spandancoder2)

[spandan Jambhekar](https://www.github.com/spandancoder2)

[Agustya Panwar](https://www.github.com/)

[Yashraj Dhuri](https://www.github.com/)

[Sahil Sadhwani](https://www.github.com/)

[Neon Maybe :)](https://www.github.com/)