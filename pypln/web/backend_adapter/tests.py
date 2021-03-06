# -*- coding:utf-8 -*-
#
# Copyright 2012 NAMD-EMAP-FGV
#
# This file is part of PyPLN. You can get more information at: http://pypln.org/.
#
# PyPLN is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyPLN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyPLN.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.test import TestCase
from mock import patch

from pypln.web.backend_adapter.pipelines import create_pipeline, default_pipeline

__all__ = ["CreatePipelineTest"]

class CreatePipelineTest(TestCase):

    @patch('pypln.web.backend_adapter.pipelines.PipelineManager', autospec=True)
    @patch('pypln.web.backend_adapter.pipelines.Pipeline', autospec=True)
    def test_should_create_pipelines_for_document(self, pipeline, pipeline_manager):
        pipeline_data = {"_id": "123", "id": 1}
        create_pipeline(pipeline_data)
        pipeline_manager.assert_called_with(settings.ROUTER_API,
                settings.ROUTER_BROADCAST)

        pipeline.assert_called_with(default_pipeline, data=pipeline_data)

        manager_instance = pipeline_manager.return_value
        manager_instance.start.assert_called_with(pipeline.return_value)
