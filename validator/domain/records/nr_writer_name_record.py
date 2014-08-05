from validator.domain.exceptions.field_rejected_error import FieldRejectedError
from validator.domain.exceptions.record_rejected_error import RecordRejectedError
from validator.domain.records.detail_header_record import DetailHeader
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import LANGUAGE_CODES


class NRWriterNameRecord(DetailHeader):
    FIELD_NAMES = ['Record prefix', 'Interested party ID', 'Writer name', 'Writer first name', 'Language code']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(9), regex.get_ascii_regex(160), regex.get_ascii_regex(160),
                   regex.get_alpha_regex(2, True)]

    def __init__(self, record, transaction):
        super(NRWriterNameRecord, self).__init__(record, transaction)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'NRW':
            raise RecordRejectedError('NRW record type expected', self._record)

        if self.attr_dict['Language code'] is not None and self.attr_dict['Language code'] not in LANGUAGE_CODES:
            raise FieldRejectedError('Given language code not in table', self._record, 'Language code')

    def _validate_field(self, field_name):
        if field_name == 'Writer name':
            RecordRejectedError('Writer name must be entered', self._record, field_name)