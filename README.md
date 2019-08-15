# UI_odrivetool

Tested on Ubuntu 16.04 - Python 3.5.2

Make sure you can run odrivetool and it can find odrive board connected.

## Repo setup

### Python env setup

#### 1. Setup python environment
```
python3 -m venv env
```
#### 2. Activate python source
```
source env/bin/activate
```

#### 3. Upgrade PIP installer
```
pip install --upgrade pip
```

#### 4. Install requirements

```
pip install odrive
pip install pyqtgraph
pip install pyqt5
```
##### Or just from requirements (Possible Errors)
```
pip install -r requirements.txt
```

#### 5. Run Python from terminal

**Run Python file**
```
python3 odrivetool_UI.py
```
