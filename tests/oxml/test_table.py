# encoding: utf-8

"""Unit-test suite for pptx.oxml.table module"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from pptx.oxml.ns import nsdecls
from pptx.oxml.table import CT_Table, TcRange

from ..unitutil.cxml import element


class DescribeCT_Table(object):

    def it_can_create_a_new_tbl_element_tree(self):
        """
        Indirectly tests that column widths are a proportional split of total
        width and that row heights a proportional split of total height.
        """
        expected_xml = (
            '<a:tbl %s>\n  <a:tblPr firstRow="1" bandRow="1">\n    <a:tableSt'
            'yleId>{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}</a:tableStyleId>\n '
            ' </a:tblPr>\n  <a:tblGrid>\n    <a:gridCol w="111"/>\n    <a:gri'
            'dCol w="111"/>\n    <a:gridCol w="112"/>\n  </a:tblGrid>\n  <a:t'
            'r h="222">\n    <a:tc>\n      <a:txBody>\n        <a:bodyPr/>\n '
            '       <a:lstStyle/>\n        <a:p/>\n      </a:txBody>\n      <'
            'a:tcPr/>\n    </a:tc>\n    <a:tc>\n      <a:txBody>\n        <a:'
            'bodyPr/>\n        <a:lstStyle/>\n        <a:p/>\n      </a:txBod'
            'y>\n      <a:tcPr/>\n    </a:tc>\n    <a:tc>\n      <a:txBody>\n'
            '        <a:bodyPr/>\n        <a:lstStyle/>\n        <a:p/>\n    '
            '  </a:txBody>\n      <a:tcPr/>\n    </a:tc>\n  </a:tr>\n  <a:tr '
            'h="223">\n    <a:tc>\n      <a:txBody>\n        <a:bodyPr/>\n   '
            '     <a:lstStyle/>\n        <a:p/>\n      </a:txBody>\n      <a:'
            'tcPr/>\n    </a:tc>\n    <a:tc>\n      <a:txBody>\n        <a:bo'
            'dyPr/>\n        <a:lstStyle/>\n        <a:p/>\n      </a:txBody>'
            '\n      <a:tcPr/>\n    </a:tc>\n    <a:tc>\n      <a:txBody>\n  '
            '      <a:bodyPr/>\n        <a:lstStyle/>\n        <a:p/>\n      '
            '</a:txBody>\n      <a:tcPr/>\n    </a:tc>\n  </a:tr>\n</a:tbl>\n'
            % nsdecls('a')
        )
        tbl = CT_Table.new_tbl(2, 3, 334, 445)
        assert tbl.xml == expected_xml

    def it_provides_access_to_its_tc_elements(self):
        tbl_cxml = 'a:tbl/(a:tr/(a:tc,a:tc),a:tr/(a:tc,a:tc))'
        tbl = element(tbl_cxml)
        tcs = tbl.xpath('.//a:tc')

        assert tbl.tc(0, 0) is tcs[0]
        assert tbl.tc(0, 1) is tcs[1]
        assert tbl.tc(1, 0) is tcs[2]
        assert tbl.tc(1, 1) is tcs[3]


class DescribeTcRange(object):

    def it_knows_when_tcs_are_in_the_same_tbl(self, in_same_table_fixture):
        tc, other_tc, expected_value = in_same_table_fixture
        tc_range = TcRange(tc, other_tc)

        in_same_table = tc_range.in_same_table

        assert in_same_table is expected_value

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[True, False])
    def in_same_table_fixture(self, request):
        expected_value = request.param
        tbl = element('a:tbl/a:tr/(a:tc,a:tc)')
        other_tbl = element('a:tbl/a:tr/(a:tc,a:tc)')
        tc = tbl.xpath('//a:tc')[0]
        other_tc = (
            tbl.xpath('//a:tc')[1] if expected_value
            else other_tbl.xpath('//a:tc')[1]
        )
        return tc, other_tc, expected_value
