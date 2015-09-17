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

from manager_rest import archiving
from manager_rest import manager_exceptions

from testenv import TestCase


class WorkflowBaseTest(TestCase):

    def _generate_archive_file(self, archive_type=None):
        archive_file_path = tempfile.mktemp(suffix=archive_type or 'tar.gz')
        archiving.make_targzfile(archive_file_path, os.path.realpath(__file__))
        return archive_file_path

    def _upload_plugin(self, plugin_id=None, archive_type=None):
        temp_file_path = self._generate_archive_file(archive_type=archive_type)
        response = self.client.plugins.upload(temp_file_path, plugin_id
                                              or uuid.uuid4())
        os.remove(temp_file_path)
        return response

    def assert_bad_parameter_error(self, fields, e):
        self.assertEqual(400, e.status_code)
        error = manager_exceptions.BadParametersError
        self.assertEquals(error.BAD_PARAMETERS_ERROR_CODE, e.error_code)
        for filter_val in fields:
            self.assertIn(filter_val,
                          e.message,
                          'expecting available filter names be contained '
                          'in error message {0}'.format(e.message))
