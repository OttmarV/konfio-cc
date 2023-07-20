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

After installing the requirements in the host computer, after executing the inital command through a CLI a docker compose with two containers is created. One container is a PostgresSQL database and after its initialization, the other container is being executed, this one has a Centos7 with python image that runs the app. 

After its execution, the database container will stay up but the centos container will shut down. To take a look at the steps executed, you can inspect them through the CLI.
At the end, a plot will be created as an image with the data extracted and transformed. 

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
      > The actual command to execute the docker cluster is 
      `docker compose up`, however extra functionality was added to pass parameters as environment variables so the extraction can be customized for a different date range, coin and currency. To review the logs after execution see section [Logs](##Logs).

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

## Logs
