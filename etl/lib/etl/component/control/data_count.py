<<<<<<< TREE
# -*- encoding: utf-8 -*-
##############################################################################
#
#    ETL system- Extract Transfer Load system
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import etl

class control_count(etl.component):
    """
    ETL Data Count Control Component:
    * calculate total of tranfering data

    """
    def process(self):
        datas = {}
        for channel,trans in self.input_get().items():
            for iterator in trans:
                for d in iterator:
                    datas.setdefault(channel, 0)
                    datas[channel] += 1

        for d in datas:
            yield {'channel': d, 'count': datas[d]}, 'main'

=======
# -*- encoding: utf-8 -*-
##############################################################################
#
#    ETL system- Extract Transfer Load system
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
"""
    ETL Data Count Control Component:
    * calculate total of tranfering data

"""

from etl import etl

class control_count(etl.component):
    """
    ETL Data Count Control Component:
    * calculate total of tranfering data

    """
    _name='etl.component.control.data_count'  
    _description='calculate total of tranfering data.'   
    _author='tiny'

    def process(self):
        datas = {}
        for channel,trans in self.input_get().items():
            for iterator in trans:
                for d in iterator:
                    datas.setdefault(channel, 0)
                    datas[channel] += 1

        for d in datas:
            yield {'channel': d, 'count': datas[d]}, 'main'

>>>>>>> MERGE-SOURCE
