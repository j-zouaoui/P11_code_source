from locust import HttpUser, task

class ProjectPerfTest(HttpUser):

    @task(6)
    def home(self):
        self.client.get("/")

    @task()
    def login(self):
        self.client.post('/showSummary',{'email': "john@simplylift.co"})

    @task()
    def login(self):
        self.client.post('/purchasePlaces',{"competition": "Spring Festival", "club": "Simply Lift", "places": "3"})
