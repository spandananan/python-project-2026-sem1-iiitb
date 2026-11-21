from fastapi import FastAPI,HTTPException
import json
from pydantic import BaseModel,Field
from datetime import datetime
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
PASS_DIR = os.path.join(CURRENT_DIR, "pass.json")

class Event(BaseModel):
    title: str | None = None
    password: str | None = None
    description: str | None = None
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

class Member(BaseModel):
    members: list[str] | None = None
    isCore: bool | None = None

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

## TODO -> ADD CAPABILITY FOR JSON TO BE CREATED IF IT DOES NOT EXIST (BUT THIS REQUIRES EVENT AND CLUB DETAILS TO BE INSIDE OF THE MAIN.PY)
def load_data():
    with open(DATA_DIR, "r", encoding="utf-8") as file:
            return json.load(file)

def find_position(club : str):
    data = load_data()
    for i in range(len(data)):
        if club.strip().lower() in data[i]["club"].strip().lower():
            return i
    return -1

def check_password(club , password):
    with open(PASS_DIR, "r", encoding="utf-8") as file:
                data=  json.load(file)
                if(data[find_position(club)]['pass'] == password):
                    return True
                else: return False

#TODO -> If two events happen to have the event str inside of them, only the first one turns up. Do I wanna fix it this?
def find_position_of_event(event: str, club: str):
    data = load_data()
    for i in range(len(data[find_position(club)]["events"])):
    #data([find_position(club)]["events"] is a list, then in that list are dictionaries
        if event.strip().lower() in data[find_position(club)]["events"][i]["title"].strip().lower():
            return i
    raise HTTPException(status_code=404, detail="Event not found (position of event)")
    
def sortByDate(lst):
    return sorted(lst, key=lambda x: datetime.strptime(x['date'], '%d-%m-%Y'), reverse=False)

def searchInList(key , list , target):
    for i in list:
        if i[key] == target:
            return True
        else: return False

def find_member_position(club : str , member : str):
    data = load_data()
    if (find_position(club) != -1):
        for i in range(len(data[find_position(club)]["members"])):
            if (data[find_position(club)]["members"][i]["name"].lower().strip() == member.lower().strip()):
                 return i

        return -1
    else:
        raise HTTPException(status_code = 404 , details = "Club not found.")         # Use in @app.patch doubtfull to me .        

def save_data(data):
    with open(DATA_DIR, "w" , encoding = "utf-8") as file:                     # This is the code for saving the data in file DATA_DIR .
        json.dump(DATA_DIR, data, indent = 8)

#---------------------------------------------------------------------------------------------------------------------------------------------------

#GET EVENT DETAILS
@app.get("/events", summary="Get All Events", response_model=list[Event] )
def get_event(club_name: str | None = None , date_after: Annotated[str | None , Field(pattern=r"^\d{2}-\d{2}-\d{4}$") ] = None , event_name: str| None=None):
    events = []
    event_search = load_data()
    for event in event_search:
        if club_name is not None and club_name.lower() not in event["club"].lower() :
            continue       

        for j in range(len(event["events"])):
            ev = event["events"][j] 

            if date_after is not None and not comes_after(ev.get("date", ""), date_after):
                continue

            if event_name is not None:
                if event_name.lower() not in ev["title"].strip().lower():
                    continue

            copy = ev.copy()
            copy["club"] = event["club"]
            events.append(copy)
    events = sortByDate(events)
    return events

#POST EVENT DETAILS
@app.post("/events" , status_code = 201)
def add_events(club: str, body: Event,password : str | None = None , role : str = "club core"):
    print(password)
    if check_password(club.lower().strip(),password):
        if role.strip().lower() in "club core":
            #Loading data from JSON
            data = load_data()
            position = find_position(club)

            if(position == -1):
                raise HTTPException(status_code=400, detail="Invalid Club")

            #Appending to events        
            event_details = body.model_dump(exclude_none = True)
            event_details.pop("password")
            data[position]["events"].append(event_details)

            #Saving the event details to the json
            with open(DATA_DIR, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=8)

        else:
            raise HTTPException(status_code=403, detail="Access Denied.")
    else:raise HTTPException(status_code=403, detail="Access Denied.")

#DELETE EVENTS
@app.delete("/events" , status_code = 204)
def delete_events(club:str = "zense",title:str|None = None,password:str|None = None, role: str = "club core"):
    if check_password(club.lower().strip(),password):
        if role.strip().lower() in "club core":
            #Loading data from JSON
            data = load_data()
            positionOfClub = find_position(club)
            positionOfEvent = find_position_of_event(title, club)

            data[positionOfClub]["events"].pop(positionOfEvent)

            with open (DATA_DIR, "w" , encoding="utf-8") as file:
                json.dump(data, file, indent = 8)

            return data 
    else: raise HTTPException(status_code=403 , detail="Access Denied.")

#PATCH EVENT DETAILS
@app.patch("/events")
def patch_events(body: Event,password:str|None = None, event: str = "Strings & Stories" , club:str = "Symphony", role: str = "club core"):
    if check_password(club.lower().strip(),password):
        if role.strip().lower() in "club core" or role.strip().lower() in "club member":
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
    else: raise HTTPException(status_code=403, detail = "Access Denied.")

# ANALYTICS : Core member , Club Member And Participant
@app.get("/analytics/core")
def number_of_events_for_each_club_core(club_name: str | None = None , core_name: str | None = None):
    core_members_of_this_club = {}
    events = load_data()
    for event in events:
        if club_name is not None and club_name.lower().strip() not in event["club"].lower():
            continue

        club_members_list = event.get("members", []) or []
        core_names_set = set()

        for j in club_members_list:
            if j.get("isCore") is True:
                core_names_set.add(j.get("name").strip().lower())

        events_of_this_club = event["events"]

        for ev in events_of_this_club:
            members_of_this_event = ev.get("members",[]) or []

            for member_name in members_of_this_event:

                if member_name.strip().lower() not in core_names_set:
                    continue

                if core_name is not None and core_name.lower().strip() != member_name.lower().strip():
                    continue

                core_members_of_this_club[member_name] = core_members_of_this_club.get(member_name,0) + 1

    return core_members_of_this_club

@app.get("/analytics/member")
def number_of_events_for_each_club_member(club_name: str | None = None , member : str | None = None):
    events_participation_of_non_core_members = {}
    data = load_data()
    for club in data:
        if club_name is not None and club_name.strip().lower() not in club["club"].strip().lower():
            continue

        club_members_list = club.get("members", []) or []
        member_set = set()

        for j in club_members_list:
            if j.get("isCore") is False:
                member_set.add(j.get("name").strip().lower())

        events_of_this_club = club["events"]

        for ev in events_of_this_club:
            volunteers_of_this_event = ev.get("volunteers",[]) or []

            for member_name in volunteers_of_this_event:

                if member_name.strip().lower() not in member_set:
                    continue

                if member is not None and member.strip().lower() not in member_name.strip().lower():
                    continue

                events_participation_of_non_core_members[member_name] = events_participation_of_non_core_members.get(member_name,0) + 1

    return events_participation_of_non_core_members

@app.get("/analytics/students")
def number_of_events_students_participated(club_name : str | None = None , student : str | None = None):
    students_participation = {}
    data = load_data()
    for club in data:
        if club_name is not None and club_name.strip().lower() not in club["club"]:
            continue

        for event in club["events"]:
            participants_of_this_event = (event["participants"])
            participants_of_this_event_set = set(event["participants"])

            for student_name in participants_of_this_event:

                if student_name not in participants_of_this_event_set:
                    continue

                if student is not None and student.strip().lower() not in student_name:
                    continue

                students_participation[student_name] = students_participation.get(student_name,0) + 1

    return students_participation

@app.get("/club")
def get_clubs(club_name:str | None = None , event_name:str|None = None,member_name:str|None = None):
    data = load_data()
    results = []
    for club in data:
        if(event_name is not None and not searchInList("events" , data , event_name)): 
            continue
        if(member_name is not None and not searchInList("members" , data , member_name)):
            continue
        if(club_name is not None and not club_name in club["club"]):
            continue
        results.append(club)
    return results

@app.post("/club")
def add_club(club_name : str):
    data = load_data()
    if (find_position(club_name) == -1):
        d = {"club" : club_name , "members" : [] , "events" : []}
        data.append(d)

        save_data(data)
    else:
        raise HTTPException(status_code = "" , details = "The club was already their.")          # Here I have doubt on status code .
    
@app.delete("/club")
def delete_club(club_name : str):
    if (find_position(club_name) != -1):
        data = load_data()
        data.pop(find_position(club_name))

        save_data(data)
    else:
        raise HTTPException(status_code = "" , details = "position of club not found! ")         # Here I have a doubt regarding the fact for status code .

@app.patch("/club")
def update_club_name(initial_club_name : str , new_club_name : str):

    if (find_position(initial_club_name) != -1):
        data = load_data()
        data[find_position(initial_club_name)]["club"] = new_club_name

        save_data(data)
    else:
        raise HTTPException(status_code = "" , details = "club not found! ")  # Here I have status code doubts.

@app.post("/club_member/volunteer")                                       #doubts in this .
def add_volunteer(club_name : str , volunteer : str , event : str):
    data = load_data()
    if (find_position(club_name) != -1) and (find_position_of_event(event , club_name) != -1):
        data[find_position(club_name)]["events"][find_position_of_event(event , club_name)]["volunteers"].append(volunteer)
        #saving via functions .
        save_data(data)
    else:
            raise HTTPException(status_code=404, detail="Event not found (position of event)")

@app.get("/{club_name}/{event_name}/volunteers")
def get_volunteer_name_for_event(event_name : str , club_name : str):
     data = load_data()
     if (find_position(club_name) != -1) and (find_position_of_event(event_name , club_name) != -1):
          return data[find_position(club_name)]["events"][find_position_of_event]["volunteers"]
     else:
          raise HTTPException(status_code = 404 , detail = "Event not found or volunteers not initialised")

@app.post("/{club_name}/club_member")
def add_club_member(club_name : str , mem_body : Member):
     data = load_data()
     if(find_position(club_name) != -1):
          d = mem_body.model_dump(exclude_none = True)
          data[find_position(club_name)]["members"].append(d)

     save_data(data)

@app.patch("/{club_name}/club_member")
def update_club_member(club_name : str , body : Member):
    data = load_data()
    d = body.model_dump(exclude_none = True)
    if (find_member_position(club_name , d["name"]) != -1):
        data[find_position(club_name)]["member"][find_member_position(club_name , d["name"])].update(d)

        save_data(data)

@app.delete("/{club_name}/club_member")
def del_club_member(club_name : str , club_member : str):
    data = load_data()
    if (find_member_position(club_name , club_member) != -1):
        data[find_position(club_name)]["members"].pop(find_member_position(club_name , club_member))

    save_data(data)
