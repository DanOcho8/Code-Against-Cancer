from locust import HttpUser, task, between
import re


"""
class HelloWorldUser(HttpUser):
   wait_time = between(0.5, 2.5)


   @task
   def access_protected_resource(self):
       # Step 1: Fetch the login page to get the CSRF token
       response = self.client.get("/accounts/login/")
       csrf_token = re.search(r'name="csrfmiddlewaretoken" value="(.*?)"', response.text).group(1)


       # Step 2: Login with the CSRF token
       response = self.client.post(
           "/accounts/login/",
           data={
               "username": "danielochoa",
               "password": "Henry1225$",
               "csrfmiddlewaretoken": csrf_token
           },
           headers={"Referer": "http://127.0.0.1:8000/accounts/login/"}
       )


       # Step 3: Access the protected resource if login was successful
       if response.status_code == 200:
           self.client.get("/resources/")
"""
class RecipesUser(HttpUser):
   wait_time = between(0.5, 2.5)


   @task
   def access_recipes_page(self):
       # Step 1: Fetch the login page to get the CSRF token
       login_response = self.client.get("/accounts/login/")
       csrf_token = re.search(r'name="csrfmiddlewaretoken" value="(.*?)"', login_response.text).group(1)


       # Step 2: Login with the CSRF token
       login_post = self.client.post(
           "/accounts/login/",
           data={
               "username": "danielochoa",
               "password": "Henry1225$",
               "csrfmiddlewaretoken": csrf_token
           },
            headers={"Referer": "http://127.0.0.1:8000/accounts/login/"}
       )


       # Step 3: If login is successful, access the recipes page
       if login_post.status_code == 200:
           # Fetch the recipes page
           response = self.client.get("/recipes/")
           if response.status_code == 200:
               # Simulate submitting a search query
               self.search_recipes()


   def search_recipes(self):
       # Simulate a search query for recipes
       search_response = self.client.get("/recipes/?query=chicken")
       if search_response.status_code == 200:
           print("Search successful")


       # Simulate pagination
       self.paginate_results()


   def paginate_results(self):
       # Simulate navigating through paginated results
       next_page_response = self.client.get("/recipes/?query=chicken&page=2")
       if next_page_response.status_code == 200:
           print("Next page loaded successfully")
