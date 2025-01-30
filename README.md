# PennyPilot

## Prerequisites

- Git - Install [here](https://git-scm.com/downloads) 
- MongoDB Shell - Install [here](https://www.mongodb.com/try/download/shell)
- Node.js - Install [here](https://nodejs.org/en)

## Setting Up

1. Create an empty folder named `pennypilot`.

2. Open a terminal in that folder (this can be done in most operating systems by simply right-clicking in an empty space in the folder and clicking a prompt such as "Open in Terminal") and use these commands:

    - `npm i -g nodemon`
    - `git init`
    - `git remote add origin https://github.com/sesartrumpet/cs386-pennypilot.git`
    - `git pull origin main`
    - `npm i`
    - `cd frontend`
    - `npm i`
    - `cd ../`
    - `mongosh`
    - `use pennypilotDB`

    You now have an instance of MongoDB running, which will be your own local database for the project.

3. Open a new terminal in the `pennypilot` folder while keeping the other terminal open and type:

    - `npm start`

    This runs the frontend and backend simultaneously. Though it should open automatically, you can view the project by visiting http://localhost:3000/ in your preferred web browser. Changes made in the project should be refreshed automatically as well.