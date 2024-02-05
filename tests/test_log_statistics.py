# -*- coding: utf-8 -*- {{{
# ===----------------------------------------------------------------------===
#
#                 Installable Component of Eclipse VOLTTRON
#
# ===----------------------------------------------------------------------===
#
# Copyright 2024 Battelle Memorial Institute
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# ===----------------------------------------------------------------------===
# }}}

import json
import os

import pytest
from mock import MagicMock
from volttron.client.messaging.health import STATUS_GOOD
from volttron.client.vip.agent import Agent
from volttrontesting.fixtures.volttron_platform_fixtures import volttron_instance

test_config = {
    "analysis_interval_sec": 2,
    "publish_topic": "platform/log_statistics",
    "historian_topic": "analysis/log_statistics"
}

@pytest.fixture(scope="module")
def publish_agent(request, volttron_instance):
    test_config = {
        "file_path": os.path.join(volttron_instance.volttron_home, "volttron.log"),
        "analysis_interval_sec": 2,
        "publish_topic": "platform/log_statistics",
        "historian_topic": "analysis/log_statistics"
    }
    # 1: Start a fake agent to publish to message bus
    agent = volttron_instance.build_agent()

    agent.callback = MagicMock(name="callback")
    agent.callback.reset_mock()

    agent.vip.pubsub.subscribe(peer='pubsub',
                               prefix=test_config.get("publish_topic"),
                               callback=agent.callback).get()

    def stop_agent():
        print("In teardown method of publish_agent")
        if isinstance(agent, Agent):
            agent.core.stop()

    request.addfinalizer(stop_agent)
    return agent

def test_log_stats(volttron_instance, publish_agent):
    test_config["file_path"] = volttron_instance.log_path
    print(f"File path: {test_config['file_path']}")

    stats_uuid = volttron_instance.install_agent(
        agent_dir="volttron-log-statistics",
        config_file=test_config,
        start=True,
        vip_identity="health_test")

    import gevent
    gevent.sleep(1)

    # building another agent should populate the logs
    volttron_instance.build_agent(identity="log_populate")

    gevent.sleep(1)

    assert publish_agent.callback.call_count >= 1

    volttron_instance.remove_agent(stats_uuid)
