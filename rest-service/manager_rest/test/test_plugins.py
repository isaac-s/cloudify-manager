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
import tempfile
import os
import uuid

from base_test import BaseServerTestCase
from cloudify_rest_client.exceptions import CloudifyClientError

from manager_rest import archiving
from manager_rest import models
from manager_rest import manager_exceptions

# todo(adaml): test put 2 plugins with same id,
# test supported types


class PluginsTest(BaseServerTestCase):
    """
    Test plugins upload and download.
    """
    def _upload_plugin(self,):
        plugin_id = uuid.uuid4()
        temp_file_path = self._generate_archive_file()
        response = self.put_file('/plugins/{0}/archive'.format(plugin_id),
                                 temp_file_path)
        os.remove(temp_file_path)
        return response

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

    def test_plugins_list_non_existing_filters(self):
        filter_fields = {'non_existing_field': 'just_some_value'}
        try:
            self.client.plugins.list(**filter_fields)
            self.fail('Expecting \'CloudifyClientError\' to be raised')
        except CloudifyClientError as e:
            self.assert_bad_parameter_error(models.Plugin.fields, e)

    def test_plugins_list_no_filters(self):
        first_plugin_response = self._upload_plugin().json
        sec_plugin_response = self._upload_plugin().json
        response = self.client.plugins.list()
        self.assertEqual(2, len(response), 'expecting 2 plugin results, '
                                           'got {0}'.format(len(response)))

        for plugin in response:
            self.assertIn(plugin['id'],
                          (first_plugin_response['id'],
                           sec_plugin_response['id']))
            self.assertIn(plugin['uploaded_at'],
                          (first_plugin_response['uploaded_at'],
                           sec_plugin_response['uploaded_at']))

    def assert_bad_parameter_error(self, fields, e):
        self.assertEqual(400, e.status_code)
        error = manager_exceptions.BadParametersError
        self.assertEquals(error.BAD_PARAMETERS_ERROR_CODE, e.error_code)
        for filter_val in fields:
            self.assertIn(filter_val,
                          e.message,
                          'expecting available filter names be contained '
                          'in error message {0}'.format(e.message))

    def _generate_archive_file(self):
        archive_file_path = tempfile.mktemp(suffix='tar.gz')
        archiving.make_targzfile(archive_file_path, os.path.realpath(__file__))
        return archive_file_path
