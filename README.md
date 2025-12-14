# SQL Injection
Below are the steps to build the container using docker compose and executing the python script.  The python script will load the JSON config file from ./config/config.json which loads in the connection parameters to connect to the MySQL container running and also the queries that the python script will execute.  The python script will write separate output files to the /output folder in the project, however I have added /output/* to the .gitignore so that my own output files are not committed to the remote repo, so definitely run the 'Execute the Python script' command below to see the script in action and view the output files and summary.

*You might have to run the command "mkdir output" in the root directory because of my .gitignore so the DataQueryTool class has a valid path to write to

## Build the Docker images
docker-compose build

## Start the containers
docker-compose up -d

# Check if containers are running
docker-compose ps

# View MySQL logs to ensure it's initialized
docker-compose logs mysql

# Execute the Python script
docker-compose exec app python /app/python/app.py

# Or run it this way
docker exec -it python_app python /app/python/app.py

# List output files
ls -la output/

