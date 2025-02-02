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

from polyaxon.connections.aws.base import get_aws_client, get_aws_resource
from polyaxon.connections.base import BaseService
from polyaxon.connections.reader import get_connection_context_path
from polyaxon.exceptions import PolyaxonConnectionError


class AWSService(BaseService):

    ENCRYPTION = "AES256"
    RESOURCE_TYPE = ""

    def __init__(self, connection=None, resource=None, **kwargs):
        super().__init__(connection=connection, **kwargs)
        if not self.RESOURCE_TYPE:
            raise PolyaxonConnectionError("Aws connection requires a RESOURCE_TYPE")
        self._resource = resource
        self._encoding = kwargs.get("encoding", "utf-8")
        self._endpoint_url = (
            kwargs.get("endpoint_url")
            or kwargs.get("aws_endpoint_url")
            or kwargs.get("AWS_ENDPOINT_URL")
        )
        self._aws_access_key_id = (
            kwargs.get("access_key_id")
            or kwargs.get("aws_access_key_id")
            or kwargs.get("AWS_ACCESS_KEY_ID")
        )
        self._aws_secret_access_key = (
            kwargs.get("secret_access_key")
            or kwargs.get("aws_secret_access_key")
            or kwargs.get("AWS_SECRET_ACCESS_KEY")
        )
        self._aws_session_token = (
            kwargs.get("session_token")
            or kwargs.get("aws_session_token")
            or kwargs.get("AWS_SECURITY_TOKEN")
        )
        self._region_name = (
            kwargs.get("region") or kwargs.get("aws_region") or kwargs.get("AWS_REGION")
        )
        self._aws_verify_ssl = kwargs.get(
            "verify_ssl",
            kwargs.get("aws_verify_ssl", kwargs.get("AWS_VERIFY_SSL", None)),
        )
        self._aws_use_ssl = (
            kwargs.get("use_ssl")
            or kwargs.get("aws_use_ssl")
            or kwargs.get("AWS_USE_SSL")
        )
        self._aws_legacy_api = (
            kwargs.get("legacy_api")
            or kwargs.get("aws_legacy_api")
            or kwargs.get("AWS_LEGACY_API")
        )

    def set_connection(
        self,
        connection=None,
        connection_type=None,
        endpoint_url=None,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        aws_session_token=None,
        region_name=None,
        aws_use_ssl=True,
        aws_verify_ssl=None,
    ):
        """
        Sets a new connection.

        Args:
            endpoint_url: `str`. The complete URL to use for the constructed client.
            aws_access_key_id: `str`. The access key to use when creating the client.
            aws_secret_access_key: `str`. The secret key to use when creating the client.
            aws_session_token: `str`. The session token to use when creating the client.
            region_name: `str`. The name of the region associated with the client.
                A client is associated with a single region.

        Returns:
            Service client instance
        """
        if connection:
            self._connection = connection
            return
        connection_type = connection_type or self._connection_type
        connection_name = connection_type.name if connection_type else None
        context_path = get_connection_context_path(name=connection_name)
        self._connection = get_aws_client(
            self.RESOURCE_TYPE or self.resource,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name,
            aws_use_ssl=aws_use_ssl,
            aws_verify_ssl=aws_verify_ssl,
            context_path=context_path,
        )

    def set_env_vars(self):
        if self._endpoint_url:
            os.environ["AWS_ENDPOINT_URL"] = self._endpoint_url
        if self._aws_access_key_id:
            os.environ["AWS_ACCESS_KEY_ID"] = self._aws_access_key_id
        if self._aws_secret_access_key:
            os.environ["AWS_SECRET_ACCESS_KEY"] = self._aws_secret_access_key
        if self._aws_session_token:
            os.environ["AWS_SECURITY_TOKEN"] = self._aws_session_token
        if self._region_name:
            os.environ["AWS_REGION"] = self._region_name
        if self._aws_use_ssl is not None:
            os.environ["AWS_USE_SSL"] = self._aws_use_ssl
        if self._aws_verify_ssl is not None:
            os.environ["AWS_VERIFY_SSL"] = self._aws_verify_ssl
        if self._aws_legacy_api:
            os.environ["AWS_LEGACY_API"] = self._aws_legacy_api

    @property
    def resource(self):
        if self._resource is None:
            self.set_resource(
                endpoint_url=self._endpoint_url,
                aws_access_key_id=self._aws_access_key_id,
                aws_secret_access_key=self._aws_secret_access_key,
                aws_session_token=self._aws_session_token,
                region_name=self._region_name,
            )
        return self._resource

    def set_resource(
        self,
        connection_type=None,
        endpoint_url=None,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        aws_session_token=None,
        region_name=None,
    ):
        """
        Sets a new resource.

        Args:
            connection_type: V1ConnectionType. The connection name to resolve.
            endpoint_url: `str`. The complete URL to use for the constructed client.
            aws_access_key_id: `str`. The access key to use when creating the client.
            aws_secret_access_key: `str`. The secret key to use when creating the client.
            aws_session_token: `str`. The session token to use when creating the client.
            region_name: `str`. The name of the region associated with the client.
                A client is associated with a single region.

        Returns:
             Service resource instance
        """
        connection_type = connection_type or self._connection_type
        connection_name = connection_type.name if connection_type else None
        context_path = get_connection_context_path(name=connection_name)
        self._resource = get_aws_resource(
            self.RESOURCE_TYPE or self.resource,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name,
            context_path=context_path,
        )
