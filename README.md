
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
$ docker run -p -d --rm 8000:8000 --name=dynamodb amazon/dynamodb-local -jar DynamoDBLocal.jar
```


#### Run the flask webserver
```bash
$ python movies_app/app.py
```
