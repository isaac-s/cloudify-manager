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
from manager_rest.responses import (BlueprintState,  # NOQA
                                    Execution,  # NOQA
                                    Deployment,  # NOQA
                                    DeploymentModification,  # NOQA
                                    Node,  # NOQA
                                    NodeInstance)  # NOQA
from flask.ext.restful import fields
from flask_restful_swagger import swagger


@swagger.model
class Plugin(object):
    resource_fields = {
        'id': fields.String,
        'uploaded_at': fields.String,
        'version': fields.String
    }

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.uploaded_at = kwargs['uploaded_at']
        self.version = kwargs['version']
