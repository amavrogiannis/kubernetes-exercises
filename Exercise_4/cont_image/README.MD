## Flask App
This directory holds the Flask application and the Dockefile, which will build the app to a container. 

The python code, which will pick the env variables and share it to the web app: 
```python
from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def home():
    user_var = os.getenv("TV_ENV")
    return render_template('index.html', user_var=user_var)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```
Where the html file will take the TV_ENV via `user_var`.
```html
<html>
<body>
    <p style="font-family: helvetica;">The stored user variable is: <b>{{ user_var }}</b></p>
</body>
</html>
```
To test it on your localhost, export the FLASK_APP=[path]
```bash
export FLASK_APP=flask_app
```
Finally, we realise your container needs to install `flask` module. Which should list to the requirements.txt file:
```text
Flask==2.2.2
```
Which makes it, the `Dockerfile` look like this:
```Dockerfile
FROM python:3.8-slim-buster # Here docker will pull the light weight of python.

ENV FLASK_APP=app # Compared against ARG, you set flask to run the /app directory inside the container.

COPY /flask_app/requirements.txt /app/requirements.txt #Copying requirements.txt source >> destination

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt # Installing modules listed in requirements.txt using pip. 

COPY flask_app/ app/ # Copying the flask files source/ destination/

EXPOSE 5000 # Exposing port.

CMD [ "python3", "app/app.py" ] # When the above are done, run `python3 app/app.py` to operate app.
```
Then to build the container, run the following being in the same path on the docker file: 
```bash
docker build . -t [image_name]:[tag_version]
```

Then run the below to confirm the image is built: 
```bash
docker images
```