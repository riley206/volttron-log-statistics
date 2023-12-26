# volttron-log-statistics

The Log Statistics agent periodically reads the "volttron.log" file based on the configured interval, computes the size 
delta from the previous hour and publishes the difference in bytes with a timestamp.  It also publishes standard 
deviation of the size delta every 24 hours.  This agent can be useful for detecting unexpected changes to the system 
which may be an indication of some sort of failure or breach.

# Prerequisites

* Python 3.8

## Python

<details>
<summary>To install Python 3.8, we recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.8
pyenv install 3.8.10

# make it available globally
pyenv global system 3.8.10
```
</details>

# Installation

1. Create and activate a virtual environment.

```shell
python -m venv env
source env/bin/activate
```

2. Install volttron and start the platform.

```shell
pip install volttron

# Start platform with output going to volttron.log
volttron -vv -l volttron.log &
```
3. Create a config directory and navigate to it:

```shell
mkdir config
cd config
```
### Configuration

4. Navigate to the config directory and create a file called `log_stat_config.json` and add the following JSON to it:

```json
{
    "file_path" : "~/volttron/volttron.log",
    "analysis_interval_sec" : 60,
    "publish_topic" : "platform/log_statistics",
    "historian_topic" : "record/log_statistics"
}
```

5. Install and start the log statistics agent
```bash
vctl install volttron-log-statistics --agent-config log_stat_config.json --json --vip-identity platform.log_statistics --start --force
```

The Log Statistics agent has 4 required configuration values:

- `file_path`:  This should be the path to the "volttron.log" file
- `analysis_interval_secs`:  The interval in seconds between publishing the size delta statistic to the message bus
- `publish_topic`:  Can be used to specify a topic to publish log statistics to which does not get captured by the 
  historian framework (topics not prefixed by any of: "datalogger", "record", "analysis", "devices")
- `historian_topic`:  Can be used to specify a topic to publish log statistics to which gets captured by the 
  historian framework ("datalogger", "record", "analysis", "devices")




### Periodic Publish


The Log Statistics agent will run statistics publishes automatically based on the configured intervals.

The following is an example of a periodic size delta publish:

```
Peer: pubsub
Sender: platform.log_statistics
Bus:
Topic: heartbeat/platform.log_statistics
Headers: {'TimeStamp': '2023-12-26T21:05:06.675246+00:00', 'min_compatible_version': '3.0', 'max_compatible_version': ''}
Message: {'log_size_delta': 6059, 'timestamp': '2023-12-26T21:05:10.627008Z'}
```

# Disclaimer Notice

This material was prepared as an account of work sponsored by an agency of the
United States Government.  Neither the United States Government nor the United
States Department of Energy, nor Battelle, nor any of their employees, nor any
jurisdiction or organization that has cooperated in the development of these
materials, makes any warranty, express or implied, or assumes any legal
liability or responsibility for the accuracy, completeness, or usefulness or any
information, apparatus, product, software, or process disclosed, or represents
that its use would not infringe privately owned rights.

Reference herein to any specific commercial product, process, or service by
trade name, trademark, manufacturer, or otherwise does not necessarily
constitute or imply its endorsement, recommendation, or favoring by the United
States Government or any agency thereof, or Battelle Memorial Institute. The
views and opinions of authors expressed herein do not necessarily state or
reflect those of the United States Government or any agency thereof.