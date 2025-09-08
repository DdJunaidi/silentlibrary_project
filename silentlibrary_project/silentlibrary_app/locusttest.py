from locust import HttpUser, TaskSet, task, between

class UserTasks(TaskSet):
    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def contact(self):
        self.client.get("/contact")

    @task(3)
    def about(self):
        self.client.get("/books")
        self.client.get("/books/1/")
        self.client.get("/books/1/reviews")

    @task(2)
    def register(self):
        self.client.get("/register")
        self.client.post("/register", {
            "username": "testuser",
            "password": "testpass",
            "email": "test@example.com"
        })

    @task(3)
    def logout(self):
        self.client.get("/accounts/logout")

    @task(3)
    def login(self):
        self.client.get("/accounts/login")
        self.client.post("/accounts/login", {
            "username": "testuser",
            "password": "testpass"
        })

    @task(1)
    def dashboard(self):
        self.client.get("/me/")
        self.client.get("/me/profile/")

    @task(1)
    def admin_area(self):
        self.client.get("/min/")
        self.client.get("/min/books/")
        self.client.get("/min/books/new/")
        self.client.post("/min/books/new/", {
            "title": "New Book",
            "author": "Author Name",
            "description": "Book description"
        })
        self.client.get("/min/books/1/edit/")
        self.client.post("/min/books/1/edit/", {
            "title": "Updated Book",
            "author": "Updated Author",
            "description": "Updated description"
        })
        self.client.get("/min/users/")
        self.client.get("/min/users/1/")
        self.client.post("/min/users/1/", {
            "is_active": True,
            "is_staff": False
        })

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    tasks = [UserTasks]
    host = "http://127.0.0.1:8000"
