# volttron-log-statistics

![Passing?](https://github.com/eclipse-volttron/volttron-log-statistics/actions/workflows/run-tests.yml/badge.svg)
[![pypi version](https://img.shields.io/pypi/v/volttron-log-statistics.svg)](https://pypi.org/project/volttron-log-statistics/)

The Log Statistics agent periodically reads ".log" files based on the configured interval, computes the size delta from the previous interval and publishes the difference in bytes with a timestamp.  It also publishes the standard deviation and mean of the size delta every 24 hours.  This agent can be useful for detecting unexpected changes to the system which may be an indication of some sort of failure or breach.

## Requires

* python >= 3.10
* volttron >= 10.0

## Installation

Before installing, VOLTTRON should be installed and running.  Its virtual environment should be active.
Information on how to install of the VOLTTRON platform can be found
[here](https://github.com/eclipse-volttron/volttron-core).

Create a directory called `config` and use the change directory command to enter it.

```shell
mkdir config
cd config
```

After entering the config directory, create a file called `log_stat_config.json`. Use the below configuration section to populate your new file.

### Configuration

The Log Statistics agent has 4 configuration parameters, all of which are required:

- `file_path`:  The file path to the log file. If left as `null`, defaults to `'volttron.log'` located within your VOLTTRON_HOME environment variable.
- `analysis_interval_secs`: The interval in seconds between publishes of the size delta statistic to the message bus. If left as `null`, defaults to 60 seconds.
- `publish_topic`: Used to specify a topic to publish log statistics to which does not get captured by the
  historian framework (topics not prefixed by any of: "datalogger", "record", "analysis", "devices"). If left as `null`, defaults to `"platform/log_statistics"`.
- `historian_topic`:  Can be used to specify a topic to publish log statistics to which gets captured by the
  historian framework ("datalogger", "record", "analysis", "devices"). If left as `null`, defaults to `record/log_statistics`.

```json
{
  "analysis_interval_sec": 60,
  "file_path": null,
  "historian_topic": "analysis/log_statistics",
  "publish_topic": "platform/log_statistics"
}
```

Install and start the log statistics agent

```bash
vctl install volttron-log-statistics --agent-config log_stat_config.json --vip-identity platform.log_statistics --start
```

View the status of the installed agent.

```shell
vctl status
```

## Development

Please see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).

Please see the following helpful guide about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)

## Disclaimer Notice

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
