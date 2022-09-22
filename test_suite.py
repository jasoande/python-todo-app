from tests import db, Todo, client


def test_render_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "To Do App" in response.data.decode('utf-8')
                
def test_add_task_db():
    title = "Test Task 1"
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    todo = Todo.query.filter_by(title=title).first()
    assert todo.title == title
    assert todo.id == 1
    assert todo.complete == False

def test_add_post(client):
    data = {
        "title": "Test Task 2"
    }
    uri = "/add"

    response = client.post(uri, data=data)
    assert response.status_code == 302
    assert "Redirecting" in response.data.decode('utf-8')

def test_tasks_displayed_on_page(client):
    title1 = "Test Task 1"
    title2 = "Test Task 2"
    response = client.get("/")
    assert response.status_code == 200
    assert title1 in response.data.decode('utf-8')
    assert title2 in response.data.decode('utf-8')

def test_update_task_post(client):
    task_id = 2
    uri = f"/update/{task_id}"

    response = client.get(uri)
    assert response.status_code == 302
    assert "Redirecting" in response.data.decode('utf-8')

    todo = Todo.query.filter_by(id=task_id).first()
    assert todo.complete == True
    assert todo.id == task_id
    assert todo.title == "Test Task 2"

def test_delete_task():
    title = "Test Task 1"
    todo = Todo.query.filter_by(title=title).first()
    db.session.delete(todo)
    db.session.commit()
    # todo_list = Todo.query.all()
    todo_list = Todo.query.filter_by(title=title).first()
    assert not todo_list 

def test_task_not_on_page(client):
    title = "Test Task 1"
    response = client.get("/")
    assert response.status_code == 200
    assert title not in response.data.decode('utf-8')
