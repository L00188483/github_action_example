
#### Initial setup for local development

```bash

$ python3 -m venv venv/
$ source venv/bin/activate
$ pip install -r requirements.txt
```


#### Running the simple tests
```bash

$ source venv/bin/activate
$ pytest github_action_example/tests/test_github_action.py
```


#### Running the movies tests
```bash

$ source venv/bin/activate
$ pytest movies_app/tests/test_movies.py
```

#### Running ALL tests
```bash

$ source venv/bin/activate
$ pytest 
```


#### Manually Trigger a Workflow in Github
* Click the `Actions` tab
* Select the Workflow on the left ("Test Simple" or "Test Movies")
* Click "Run Workflow" on the right



#### Optional: you launch the DaynamoDB container manually
```bash
$ docker run -d --rm -p 8000:8000 --name=dynamodb amazon/dynamodb-local -jar DynamoDBLocal.jar
```

#### Optional: launch the Flask webapp
```bash
# note: ensure you have dynamodb running first
$ cd movies_app/
$ python app.py
```
* go to: http://localhost:5000/movies
* go to: http://localhost:5000/movies/2015/The_Big_New_Movie
