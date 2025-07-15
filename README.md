# Idle Outpost Claimer

A simple Python script that runs in a Docker container to automatically claim daily and weekly rewards for the game Idle Outpost from the Xsolla web store.

## Quickstart

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/IdleOutpostClaimer.git
    cd IdleOutpostClaimer
    ```

2.  **Find your `USER_GAME_ID`:**
    You need to find your unique game ID. This is usually done by monitoring network traffic from your device while the game is running. Look for requests to the game's servers.

3.  **Run the container:**
    Set your game ID in the command below and run it:
    ```bash
    docker run -d --name idle-outpost-claimer \
      -e USER_GAME_ID="YOUR_GAME_ID_HERE" \
      --restart always \
      idleoutpostclaimer:latest
    ```
    *Note: Replace `YOUR_GAME_ID_HERE` with your actual ID.*

## Configuration

### Timezone (Optional)
The script uses `Europe/Berlin` as the default timezone for logging. You can set a different one using the `TZ` environment variable. A list of valid timezones can be found [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

Example for New York time:
```bash
docker run -d --name idle-outpost-claimer \
  -e USER_GAME_ID="YOUR_GAME_ID_HERE" \
  -e TZ="America/New_York" \
  --restart always \
  idleoutpostclaimer:latest
```

## How it Works
The script runs on a schedule inside the Docker container:
- **Daily Rewards:** Claimed every day at 2:00 AM (container time).
- **Weekly Rewards:** Claimed along with the daily ones.

Logs are printed to the container's log output. You can view them with `docker logs idle-outpost-claimer`. 