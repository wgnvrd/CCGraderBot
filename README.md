# CCGraderBot
A service for assisted and automatic grading of computer science assignments at Colorado College.


## Development
### Environment setup
Create an .env file (this is included in `.gitignore`):
<!-- Might not include password in the future... -->
#### Installation
On a linux system:
```bash
git clone https://github.com/wgnvrd/CCGraderBot.git
cd CCGraderBot
touch .env
echo "CANVAS_ACCESS_TOKEN=#[YOUR CANVAS ACCESS TOKEN]" >> .env
```
The following dependencies need to be installed:
```
python-dotenv
canvasapi
junitparser
tomlkit
pathlib
slugify
```

### Usage
```bash
python Autograder.py
```

#### Configuration files
