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

from manager_rest import archiving

from base_test import BaseServerTestCase


class PluginsTest(BaseServerTestCase):
    """
    Test plugins upload and download.
    """
    def setUp(self):
        super(PluginsTest, self).setUp()
        self.plugin_id = self._upload_plugin()

    def _upload_plugin(self):
        plugin_id = 'plugin_id'
        temp_file = tempfile.mktemp()
        archiving.make_targzfile(temp_file, os.path.realpath(__file__))
        self.put_file('/plugins/{0}/archive'.format(plugin_id), temp_file)
        # self.client.plugins.download('lll', temp_file)
        # self.client.plugins.upload(temp_file, plugin_id)
        return plugin_id

    def test_plugins_upload(self):
        file_path = self._generate_archive_file()
        print file_path
        self.post_file()
        print 'a'

    def _generate_archive_file(self):
        temp_file = tempfile.mktemp()
        return temp_file
