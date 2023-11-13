import json
from locust import HttpUser, task

class MyLocustUser(HttpUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csrf_token = None

    def on_start(self):
        response = self.client.get("/")
        self.csrf_token = response.cookies["csrftoken"]
        print(self.csrf_token)

    def post_with_csrf_token(self, url, data):
        headers = {"X-CSRFToken": self.csrf_token}
        response = self.client.post(url, headers=headers, data=data)
        return response
    
    @task
    def resultado(self):
        self.on_start()
        cookie_value = json.dumps({"seleccionados": ["0", "1", "2", "3", "4", "5", "6", "7"]})
        self.client.cookies.set("IDs", cookie_value)
        response = self.post_with_csrf_token("/resultados/",{'metodo': "ingredientes"})

        # Valida la respuesta
        if response.status_code == 200:
             print("validada")

    @task
    def detalle(self):
        self.on_start()
        self.client.get("/receta/44")
