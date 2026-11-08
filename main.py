from fastapi import FastAPI,HTTPException
import json
from pydantic import BaseModel,Field
from typing import Annotated

# Setting Up Base Model For Club,Event

class Event(BaseModel):
    title: str | None = None
    venue: str | None = None
    date: str | None = None
    members: list[str] | None = None
    guests: list[str] | None = None
    participants: list[str] | None = None
    volunteers: list[str] | None = None

class Club(BaseModel):
    members: list[str] | None = None
    events: list[Event] | None = None


# Setting Up Helper Functions
def comes_after(date1 : str , date2 : str):
    d1 = date1.split("-")
    d2 = date2.split("-")
    if(d1[2] > d2[2]):
        return True
    elif(d1[2] < d2[2]):
        return False
    if(d1[1] > d2[1]):
        return True
    elif(d1[1] < d2[1]):
        return False
    if(d1[0] > d2[0]):
        return True
    elif(d1[0] < d2[0]):
        return False
    else:
        return True
    

# Initialising App
app = FastAPI(title="EMS API PORTAL" , summary="This portal is used as server hub for EMS Website")

# CRUD Operation on Events
# TODO : Set Up Post ,Patch  ,Put ,Delete in Event

@app.get("/events", summary="used to obtain all events" , response_model=list[Event] )
def find_all_events(club_name : str | None = None, date_after:Annotated[str|None, Field(pattern=r"^\d{2}-\d{2}-\d{4}$")] = None):
    data = []
    results = []
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    for club in data:
        if(club_name is not None and club_name.lower() not in club["club"].lower()):
            continue
        for i in range(len(club["events"])):
            if(date_after is not None and not comes_after(club["events"][i]["date"], date_after)):
                        continue
            results.append(club["events"][i])
    return results

