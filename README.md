# Cooking Bot Backend App

## Set up and run App

First create a virtual machine:

```
python3 -m venv venv
```

Then use  `source venv/bin/activate` to enter into the VM and you can use `deactivate` to leave the VM.

Install the required dependencies:
```
 pip3 install -r requirements.txt
```

If adding a new dependency be sure to use to save it as a requirement:
```
pip freeze > requirements.txt
```

Run the app with: 
```
flask run
```