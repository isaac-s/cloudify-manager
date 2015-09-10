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
from base_test import BaseServerTestCase


class PluginsTest(BaseServerTestCase):
    """
    Test plugins upload and download.
    """
    def test_get_plugin_by_id(self):
        put_plugin_response = self._upload_plugin().json
        get_plugin_by_id_response = self.client.plugins.get(
            put_plugin_response['id'])
        self.assertEquals(put_plugin_response,
                          get_plugin_by_id_response)

    def test_delete_plugin(self):
        put_plugin_response = self._upload_plugin().json
        plugins = self.client.plugins.list()
        self.assertEqual(1, len(plugins), 'expecting 1 plugin result, '
                                          'got {0}'.format(len(plugins)))
        get_plugin_by_id_response = self.client.plugins.delete(
            put_plugin_response['id'])
        self.assertEquals(put_plugin_response,
                          get_plugin_by_id_response)
        plugins = self.client.plugins.list()
        self.assertEqual(0, len(plugins), 'expecting 0 plugin result, '
                                          'got {0}'.format(len(plugins)))

    def test_plugins_list_with_filters(self):
        self._upload_plugin().json
        sec_plugin_id = self._upload_plugin().json['id']
        filter_field = {'id': sec_plugin_id}
        response = self.client.plugins.list(**filter_field)

        self.assertEqual(len(response), 1, 'expecting 1 plugin result, '
                                           'got {0}'.format(len(response)))
        self.assertDictContainsSubset(filter_field, response[0],
                                      'expecting filtered results having '
                                      'filters {0}, got {1}'
                                      .format(filter_field, response[0]))

    def test_put_plugins_response_status(self):
        ok_response = self._upload_plugin(plugin_id='plugin')
        self.assertEquals('201 CREATED', ok_response._status)
        error_response = self._upload_plugin(plugin_id='plugin')
        self.assertEquals('409 CONFLICT', error_response._status)

    def test_supported_archive_types(self):
        # todo(adaml): this list should obtained from the actual module
        supported_archive_types = ['zip', 'tar', 'tar.gz', 'tar.bz2']
        for archive_type in supported_archive_types:
            response = self._upload_plugin(archive_type=archive_type)
            self.assertEquals('201 CREATED', response._status)
