# ...existing code...

import os
import sys


from app import app

client = app.test_client()

def test_home():
    res = client.get("/")
    assert res.status_code == 200

def test_create_todo():
    data = {"task": "Learn Flask"}
    res = client.post("/todo", json=data)
    assert res.status_code == 201
    assert res.get_json()["status"] == "created"

def test_get_todos():
    res = client.get("/todo")
    assert res.status_code == 200

def test_update_todo():
    data = {"task": "Updated task"}
    res = client.put("/todo/0", json=data)
    assert res.status_code == 200

def test_delete_todo():
    res = client.delete("/todo/0")
    assert res.status_code == 200
# ...existing code...