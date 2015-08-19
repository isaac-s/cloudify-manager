#########
# Copyright (c) 2015 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.


from cloudify_rest_client.exceptions import UserUnauthorizedError

from manager_rest.test.security.security_test_base import SecurityTestBase


class SecurityTest(SecurityTestBase):

    def test_secured_client(self):
        client = self.create_client(headers=SecurityTestBase.
                                    create_auth_header(username='user1',
                                                       password='pass1'))
        client.deployments.list()

    def test_wrong_credentials(self):
        client = self.create_client(headers=SecurityTestBase.
                                    create_auth_header(username='user1',
                                                       password='pass2'))
        self.assertRaises(UserUnauthorizedError, client.deployments.list)

    def test_missing_credentials(self):
        client = self.create_client(headers=SecurityTestBase.
                                    create_auth_header(username=None,
                                                       password=None))
        self.assertRaises(UserUnauthorizedError, client.deployments.list)

    def test_missing_user(self):
        client = self.create_client(headers=SecurityTestBase.
                                    create_auth_header(username=None,
                                                       password='pass1'))
        self.assertRaises(UserUnauthorizedError, client.deployments.list)

    def test_missing_password(self):
        client = self.create_client(headers=SecurityTestBase.
                                    create_auth_header(username='user1',
                                                       password=None))
        self.assertRaises(UserUnauthorizedError, client.deployments.list)

    def test_token_authentication(self):
        client = self.create_client(headers=SecurityTestBase.
                                    create_auth_header(username='user1',
                                                       password='pass1'))
        token = client.tokens.get()
        client = self.create_client(headers=SecurityTestBase.
                                    create_auth_header(token=token.value))
        client.blueprints.list()

    def test_secured_manager_blueprints_upload(self):
        client = self.create_client(headers=SecurityTestBase.
                                    create_auth_header(username='user1',
                                                       password='pass1'))
        client.blueprints.upload(self.get_mock_blueprint_path(), 'bp-id')
