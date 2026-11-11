"""Student progress API. Run: pip install fastapi uvicorn; uvicorn app:app --reload"""
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from pathlib import Path
import json
app=FastAPI(title="Student Progress Manager");DB=Path("students.json")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
def read():return json.loads(DB.read_text()) if DB.exists() else []
def write(x):DB.write_text(json.dumps(x,indent=2))
class Student(BaseModel):name:str=Field(min_length=1);course:str;attendance_percent:float=Field(ge=0,le=100);notes:str=""
@app.get("/students")
def students():return read()
@app.post("/students")
def add(s:Student):
 rows=read();r=s.model_dump();r["id"]=max([x["id"] for x in rows],default=0)+1;rows.append(r);write(rows);return r
@app.put("/students/{sid}")
def update(sid:int,s:Student):
 rows=read()
 for i,r in enumerate(rows):
  if r["id"]==sid:rows[i]={**s.model_dump(),"id":sid};write(rows);return rows[i]
 raise HTTPException(404,"Student not found")