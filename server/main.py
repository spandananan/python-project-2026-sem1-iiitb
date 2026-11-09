from fastapi import FastAPI,HTTPException
import json
from pydantic import BaseModel,Field
import os
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="EMS Server" , description="This is server page of Official IIITB EMS Server")

# Resolving CORS Permission to backend (Just assume permission to establish connection between frontend and backend) 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, "data.json")

class Event(BaseModel):
    title: str | None = None
    venue: str | None = None
    date: str | None = None
    club: str | None = None
    members: list[str] | None = None
    guests: list[str] | None = None
    participants: list[str] | None = None
    volunteers: list[str] | None = None

class Club(BaseModel):
    members: list[str] | None = None
    events: list[Event] | None = None

#HELPER FUNCTIONS
#--------------------------------------------------------------------------------------------------------------------------------------------------

def comes_after(date1 : str , date2 : str):
    d1 = list(map(int, date1.split("-")))
    d2 = list(map(int, date2.split("-")))
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

def save_data(data):
    with open(DATA_DIR, "r") as file:
        json.dump(DATA_DIR, data, indent = 8)

## TODO -> ADD CAPABILITY FOR JSON TO BE CREATED IF IT DOES NOT EXIST (BUT THIS REQUIRES EVENT AND CLUB DETAILS TO BE INSIDE OF THE MAIN.PY)
def load_data():
    with open(DATA_DIR, "r", encoding="utf-8") as file:
            return json.load(file)

def find_position(club : str):
    data = load_data()
    for i in range(len(data)):
        if club.strip().lower() in data[i]["club"].strip().lower():
            return i
    return len(data)

#TODO -> If two events happen to have the event str inside of them, only the first one turns up. Do I wanna fix it this?
def find_position_of_event(event: str, club: str):
    data = load_data()
    for i in range(len(data[find_position(club)]["events"])):
    #data([find_position(club)]["events"] is a list, then in that list are dictionaries
        if event.strip().lower() in data[find_position(club)]["events"][i]["title"].strip().lower():
            return i
    raise HTTPException(status_code=404, detail="Event not found (position of event)")
        


#---------------------------------------------------------------------------------------------------------------------------------------------------

#GET EVENT DETAILS
@app.get("/events", summary="Get All Events" , response_model=list[Event] )
async def get_events(club_name : str | None = None, date_after:Annotated[str|None, Field(pattern=r"^\d{2}-\d{2}-\d{4}$")] = None):
    data = []
    events = []
    with open(DATA_DIR , "r" , encoding="utf-8") as file:
        data = json.load(file)
    for club in data:
        if(club_name is not None and club_name.lower() not in club["club"].lower()):
            continue
        for i in range(len(club["events"])):
            if(date_after is not None and not comes_after(club["events"][i]["date"], date_after)):
                continue
            club["events"][i]["club"] = club["club"]
            events.append(club["events"][i])
    return events

#POST EVENT DETAILS
@app.post("/events")
def add_events(club: str, body: Event, role : str = "club core"):
    if role.strip().lower() in "club core":
        #Loading data from JSON
        data = load_data()
        position = find_position(club)

        #Appending to events        
        event_details = body.model_dump(exclude_none = True)
        data[position]["events"].append(event_details)

        #Saving the event details to the json
        with open(DATA_DIR, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=8)

    else:
        raise HTTPException(status_code=403, detail="Access Denied.")


#DELETE EVENTS
@app.delete("/events")
def delete_events(event: str = "Tech Triad" , club:str = "Zense", role: str = "club core"):
    if role.strip().lower() in "club core":
        #Loading data from JSON
        data = load_data()
        positionOfClub = find_position(club)
        positionOfEvent = find_position_of_event(event, club)

        data[positionOfClub]["events"].pop(positionOfEvent)

        with open (DATA_DIR, "w" , encoding="utf-8") as file:
            json.dump(data, file, indent = 8)

        return data 


#PATCH EVENT DETAILS
@app.patch("/events")
def patch_events(body: Event, event: str = "Strings & Stories" , club:str = "Symphony", role: str = "club core"):
    if role.strip().lower() in "club core" or role.strip.lower() in "club member":
        data = load_data()
        positionOfClub = find_position(club)
        positionOfEvent = find_position_of_event(event, club)

        changes = body.model_dump(exclude_none=True)

        for keys in data[positionOfClub]["events"][positionOfEvent]:
            data[positionOfClub]["events"][positionOfEvent][keys] = changes[keys]

        with open (DATA_DIR, "w" , encoding="utf-8") as file:
                    json.dump(data, file, indent = 8)

    else:
        raise HTTPException(status_code=403, detail = "Access Denied.")
