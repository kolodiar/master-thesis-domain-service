from locust import HttpUser, between, task


class ImsLoadTest(HttpUser):
    wait_time = between(0.05, 1)

    # running instance in docker-compose
    host = "http://localhost:8081"
    # path to the user endpoint
    usersRootPath = "/api/v1/users"

    # init user
    userTemplate = {
        "id": None,
        "name": "Name",
        "surname": "Surname",
        "email": "Email",
        "address": "Address"
    }

    # current locust user 'user id'
    userId = ""
    iterationsAmount = 50
    currentIteration = 1

    # Create new user to update during the following tasks
    def on_start(self):
        self.client.headers['Content-Type'] = "application/json"
        response = self.client.post(
            url=self.usersRootPath,
            json=self.userTemplate
        )
        self.userId = response.json()['id']
        print(self.userId)

    @task
    def update_user(self):
        if self.currentIteration <= 100:
            self.client.put(
                url=f"{self.usersRootPath}/{self.userId}",
                json=self.get_user_change_for_iteration(self.currentIteration),
            )
            print(f"Update request for '{self.userId}' ({self.currentIteration})")
            self.currentIteration += 1

    @staticmethod
    def get_user_change_for_iteration(iteration: int):
        return {
            "newAddress": f"Address {iteration}"
        }
