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
#

from base_list_test import BaseListTest
API_VERSION = 'v2'


class ResourceListTestCase(BaseListTest):

    def test_deployments_list_paginated_size(self):
        self._put_n_deployments(deployment_id="test",
                                number_of_deployments=10)
        first = {"_offset": 0,
                 "_size": 3}
        response = self.get('/deployments', query_params=first).json
        self.assertEqual(3, len(response), 'pagination applied, '
                                           'expecting 3 results, got {0}'
                         .format(len(response)))
        last = {"_offset": 9,
                "_size": 3}
        response = self.get('/deployments', query_params=last).json
        self.assertEqual(1, len(response), 'pagination applied, '
                                           'expecting 1 result, got {0}'
                         .format(len(response)))
        empty = {"_offset": 99,
                 "_size": 3}
        response = self.get('/deployments', query_params=empty).json
        self.assertEqual(0, len(response), 'pagination applied, '
                                           'expecting 0 results, got {0}'
                         .format(len(response)))
        no_pagination = {"_offset": 0,
                         "_size": 11}
        response = self.get('/deployments', query_params=no_pagination).json
        self.assertEqual(10, len(response), 'no pagination applied, '
                                            'expecting 10 results, got {0}'
                                            .format(len(response)))
