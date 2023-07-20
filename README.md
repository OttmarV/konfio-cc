# Coding Challenge - Bitcoin Price
Develop an automated and scalable process to obtain the average of each 5
days (moving average) of the price of bitcoin in the first quarter of 2022.

## Objective
The finance team needs to analyze the behavior of bitcoin to know if it is feasible
to invest in that currency.
Your task is to obtain this information in an automated way and be prepared for
sudden changes that must be made at the moment.

## Tasks

 - Explore Crypto API link: https://www.coingecko.com/en/api/documentation
 - Get a list of all coins with id, name and symbol (using Crypto API)
    - Get bitcoin coin id
 - Get the price of bitcoin in usd and by date of the first quarter of 2022 (using Crypto API)
 - Save the information in the database of your choice
 - Consume the data previously persisted in the database to make a
window/partition function for every 5 days (spark or pandas)
   - Extra point: Save the information in the database of your choice
 - Add your code on github repository
 - Share the link before the interview
 - Extra point: using the tool of your choice show the results obtained in a
graph


## Candidate Implementation

### Summary

This project was focused on simplicity and use of the known technologies to develop an app encapsulated in docker, which does a one time execution of it. 

Once done installing the requirements in the host computer, after executing the inital command through a CLI, a docker compose with two containers is created. One container is a PostgresSQL database and after its initialization, the other container is created, this one has a Centos7 image with python that runs the app. Both containers interact through a default network.

  On every execution, the app will recreate the tables needed (landing_coin and refined_coin). Then based on the script arguments, passed through environment variabes to the main.py python script, it will extract the coin details and use that information to actually extract the price data for the dates requested, which will be stored in the landing table. Continuing with the pipeline, the app picks up the data from the landing table, the 5 day moving average is calculated and writes it back to the refined table. The final step uses the refined data to plot the prices and moving average against the input dates, generating an image out of it and saving it in the local directory of the host machine. 

After its execution, the database container will stay up but the centos container will shut down. To take a look at the steps executed, you can inspect them through the CLI (see section [Logs](#logs)).
At the end, a plot will be created as an image with the data extracted and transformed. 

### Tech-stack
- Python
- Postgres DB
- Docker
- Git

#### Main python libraries
- pandas: latest
- matplotlib==2.9.3
- pycoingecko: latest
- sqlalchemy: latest

    > **Important**
    > For the purpose of this project, pycoingecko library is used. I would highly recommend to create your own API wrappers to avoid security breaches.

### Project Tree

- Root directory is **konfio-cc/**
- First level we find the README.md file and the src/ directory.
  - **/src/** contains all the code and docker settings.
    - docker-compose.yml: Contains the container settings to be created
  - **/src/app/** contains the code to be executed by the app.
    - Dockerfile: Settings to build the app container image
    - main.py: Python script that runs the app
    - requirements.txt: Libraries to be installed in the app docker container
    - sql_queries.py: Queries to drop and create tables needed
  - **/src/app/lib/** has the complentary python scripts to suppor the main.py execution
    - db_engine.py: Functions to connect to postgres
    - etl.py: Functions with the actual ETL specifically for the app
    - helpers.py: Suppor functions
    - plot.py: Function to create the plot and its settings

![image](https://github.com/OttmarV/konfio-cc/assets/17484897/09299802-0a18-48bc-b7e7-923cd65f78b4)

### Steps for execution

  1. Install Docker Desktop and Docker Compose according to your OS, latest version should be fine. 
  2. Download this GitHub repository.
  3. Run Docker Desktop or make sure docker's agen is up and running.
  4. Open a terminal, then change directory to **_konfio-cc/src/_** directory. 
      ```console
      foo@bar:~$ cd konfio-cc/src
      ```
  5. Execution modes

      Below commands will launch the multi-container app. This will download the required images, and will launch the containers with the services and networks needed and declared in **_konfio-cc/src/docker-compose.yml_** file. This step might take a while the first time it is executed. The following execution modes differ in how the output is being followed up. 

      > **Note**
      > The actual command to execute the docker cluster is `docker compose up`, however extra functionality was added to pass parameters as environment variables so the extraction can be customized for a different date range, coin and currency. To review the logs after execution see section [Logs](#logs).

      > **Important**
      > Mandatory environment variables are passed as arguments to the compose docker command to execute the app. These variables include: **COIN_NAME** the official name of the coin to extract, case sensitive. **CURRENCY** the currency of the prices to be extracted. **START_DATE** and **END_DATE** represent the date range of data to be extracted, both inclusive, format YYYYMMDD. 
         

      - #### Detached mode: Run containers in the background
        Execute this command tu run in detached mode, meaning the log will not show up in the terminal standard output, just the docker container status.
            
        ```console
        foo@bar:~$ COIN_NAME=Bitcoin CURRENCY=usd START_DATE=20220101 END_DATE=20220331 docker compose up -d
        ```

      - #### Atached mode: Run containers in the foreground
        Throughout the standard output, you can see the execution of the containers and the ETL steps. However after the execution is done, you might need to hit `CTRL+C` to halt the execution, and then run command `docker compose down` to remove the containers. 

        ```console
        foo@bar:~$ COIN_NAME=Bitcoin CURRENCY=usd START_DATE=20220101 END_DATE=20220331 docker compose up
        ```

  6. After the execution, an image under **_src/_** directory named **_coin_moving_average.png_** will be created using **matplotlib** library. This image is the plot to be inspected where both, the prices and moving average will be drawn against the input dates.
  
  7. To shut down the cluster, run the following command 

        ```console
      foo@bar:~$ docker compose down
      ```

## Logs
After the execution, weather it was detached or not, you can extract the logs to have a better look of the execution of both containers. These commands will create the log files in your local directory. Before getting the logs, we need the container ID for each one, so first execute this command to get the container ids:

  ```console
  foo@bar:~$ docker ps -a
  ```
Then execute these commands to create the log files, use the first one to get the database log, and the second one for the app with their corresponding container ids:

  ```console
  foo@bar:~$ docker logs <container_id &> db.log
  foo@bar:~$ docker logs <container_id &> app.log
  ```
Now you can inspect both log files. Database log will show its starting and database creation. The app log will show a step by step execution and details of the data being extracted, processed and loaded.

  ### Logging into database container
  After the execution, database container will still be running so you are able to log into it and explore the data that was ingested. The following commands will get you to the tables created by this app. 

  - Log into the database container using the container id (you can get it executing `docker ps -a` command) and enabling a bash terminal.

    ```console
    foo@bar:~$ docker exec -it <container_id> bash
    ```
  - Connect to postgres with user "postgres"
    ```console
    foo@bar:~$ psql -U postgres 
    ```
  - List all databases available
    ```console
    foo@bar:~$ \l
    ```
  - Connect to the database **db**, this one will have the data we just processed. 
    ```console
    foo@bar:~$ \c db
    ```
  - Show the tables for the database **db**
    ```console
    foo@bar:~$ \dt
    ```
  - Query the table you want and explore the data
    ```console:
    foo@bar:~$ SELECT * FROM landing_coin limit 10;
    ```
