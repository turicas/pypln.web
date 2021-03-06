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

from pypln.web.settings.base import *

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'pypln_dev',
    'gridfs_collection': 'files',
    'analysis_collection': 'analysis',
    'monitoring_collection': 'monitoring',
}

ROUTER_API = 'tcp://127.0.0.1:5555'
ROUTER_BROADCAST = 'tcp://127.0.0.1:5556'
ROUTER_TIMEOUT = 5
