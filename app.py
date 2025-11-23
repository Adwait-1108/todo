from flask import Flask, jsonify, request, render_template, redirect, flash

app = Flask(__name__)
app.secret_key = "secret123"  # needed for flash messages

# In-memory todos
# Each todo will be:
# { "task": "Learn Flask", "completed": False }
todos = []


@app.route("/")
def home_page():
    filter_type = request.args.get("filter", "all")

    if filter_type == "completed":
        filtered_todos = [t for t in todos if t["completed"]]
    elif filter_type == "pending":
        filtered_todos = [t for t in todos if not t["completed"]]
    else:
        filtered_todos = todos

    return render_template("index.html", todos=filtered_todos, filter=filter_type)


# Add Todo from HTML or API
@app.route("/todo", methods=["POST"])
def create_todo():
    if request.is_json:
        data = request.get_json()
    else:
        task = request.form.get("task")
        data = {"task": task, "completed": False}

    todos.append(data)

    # Flash message only for HTML
    if not request.is_json:
        flash("Todo added successfully!", "success")
        return redirect("/")

    return jsonify({"status": "created", "todo": data}), 201


# API: Read
@app.route("/todo", methods=["GET"])
def get_todos():
    return jsonify(todos), 200


# Edit Todo
@app.route("/todo/edit/<int:index>", methods=["POST"])
def edit_todo(index):
    if index >= len(todos):
        flash("Todo not found!", "danger")
        return redirect("/")

    new_text = request.form.get("task")
    todos[index]["task"] = new_text

    flash("Todo updated successfully!", "info")
    return redirect("/")


# Toggle Complete
@app.route("/todo/toggle/<int:index>")
def toggle_complete(index):
    if index < len(todos):
        todos[index]["completed"] = not todos[index]["completed"]
        flash("Todo status updated!", "info")
    return redirect("/")


# DELETE via HTML
@app.route("/todo/delete/<int:index>", methods=["GET"])
def delete_todo_html(index):
    if 0 <= index < len(todos):
        todos.pop(index)
        flash("Todo deleted!", "warning")
    return redirect("/")


# API DELETE (unchanged for tests)
@app.route("/todo/<int:index>", methods=["DELETE"])
def delete_todo_api(index):
    if index >= len(todos):
        return jsonify({"error": "Not found"}), 404

    deleted = todos.pop(index)
    return jsonify({"status": "deleted", "todo": deleted}), 200


# API Update (tests)
@app.route("/todo/<int:index>", methods=["PUT"])
def update_todo_api(index):
    if index >= len(todos):
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    todos[index] = data
    return jsonify({"status": "updated", "todo": data}), 200


if __name__ == "__main__":
    app.run(debug=True,port=5050)
