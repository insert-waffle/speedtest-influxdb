# Speedtest to InfluxDB

This is a modified version of [aidengilmartin's script](https://github.com/aidengilmartin/speedtest-to-influxdb). This version of the Python script that will run the Speedtest CLI application by Ookla when called by a cronjob, reformat the data output and forward it on to an InfluxDB database.
You may want to do this so that you can track your internet connections consistency over time. Using Grafana you can view and explore this data easily.

## Using the script

Adjust the InfluxDB connection settings at the top of `speedtest.py` file to fit your setup and then run with one of the options listed below.
Be aware that this script will automatically accept the license and GDPR statement so that it can run non-interactively. Make sure you agree with them before running.

### Run using crontab

1. Install the InfluxDB client for library from Python.

    `pip3 install influxdb`

2. Run the script.

    `python3 ./speedtest.py`

3. Edit crontab to make the script run every hour

    Edit crontab using your favorite editor with `crontab -e` and add the following line: `0 */1 * * * /usr/bin/python3 /path/to/script/speedtest.py`, this way the cronjob runs every hour.
	
## Grafana dashboard

Included in the repository, is JSON formatted code for a Grafana dashboard. Includes measurements from the last speedtest, data over the last 6 hours, recent locations and an image of the last speedtest that ran.

![Grafana dashboard](https://i.imgur.com/xZuH2TT.png)