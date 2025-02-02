#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

from polyaxon.env_vars.getters import get_agent_info
from polyaxon.env_vars.keys import EV_KEYS_AGENT_INSTANCE
from polyaxon.exceptions import PolyaxonAgentError
from polyaxon.utils.test_utils import BaseTestCase


class TestAgentEnvVars(BaseTestCase):
    def test_get_agent_info(self):
        with self.assertRaises(PolyaxonAgentError):
            get_agent_info(None)

        with self.assertRaises(PolyaxonAgentError):
            get_agent_info("foo")

        with self.assertRaises(PolyaxonAgentError):
            get_agent_info("foo.bar")

        with self.assertRaises(PolyaxonAgentError):
            get_agent_info("foo/bar")

        with self.assertRaises(PolyaxonAgentError):
            get_agent_info("foo/bar/moo")

        with self.assertRaises(PolyaxonAgentError):
            get_agent_info("foo.bar.moo")

        assert get_agent_info("foo.agents.moo") == ("foo", "moo")

        current = os.environ.get(EV_KEYS_AGENT_INSTANCE)
        os.environ[EV_KEYS_AGENT_INSTANCE] = "foo.agents.moo"
        assert get_agent_info("foo.agents.moo") == ("foo", "moo")
        if current:
            os.environ[EV_KEYS_AGENT_INSTANCE] = current
        else:
            del os.environ[EV_KEYS_AGENT_INSTANCE]
