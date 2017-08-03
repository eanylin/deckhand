# Copyright 2017 AT&T Intellectual Property.  All other rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from deckhand.engine import document_validation
from deckhand import errors
from deckhand.tests.unit.engine import test_document_validation


class TestDocumentValidationNegative(
        test_document_validation.TestDocumentValidationBase):
    """Negative testing suite for document validation."""

    BASIC_ATTRS = (
        'schema', 'metadata', 'data', 'metadata.schema', 'metadata.name')
    SCHEMA_ERR = ("The provided YAML failed schema validation. "
                  "Details: '%s' is a required property.")
    SCHEMA_ERR_ALT = ("The provided %s YAML failed schema validation. "
                      "Details: '%s' is a required property.")

    def _test_missing_required_sections(self, properties_to_remove):
        for idx, property_to_remove in enumerate(properties_to_remove):
            missing_prop = property_to_remove.split('.')[-1]
            invalid_data = self._corrupt_data(property_to_remove)

            if property_to_remove in self.BASIC_ATTRS:
                expected_err = self.SCHEMA_ERR % missing_prop
            else:
                expected_err = self.SCHEMA_ERR_ALT % (
                    self.data['schema'], missing_prop)

            # NOTE(fmontei): '$' must be escaped for regex to pass.
            expected_err = expected_err.replace('$', '\$')

            with self.assertRaisesRegex(errors.InvalidDocumentFormat,
                                        expected_err):
                document_validation.DocumentValidation(invalid_data)

    def test_certificate_key_missing_required_sections(self):
        self._read_data('sample_certificate_key')
        properties_to_remove = self.BASIC_ATTRS + ('metadata.storagePolicy',)
        self._test_missing_required_sections(properties_to_remove)

    def test_certificate_missing_required_sections(self):
        self._read_data('sample_certificate')
        properties_to_remove = self.BASIC_ATTRS + ('metadata.storagePolicy',)
        self._test_missing_required_sections(properties_to_remove)

    def test_data_schema_missing_required_sections(self):
        self._read_data('sample_data_schema')
        properties_to_remove = self.BASIC_ATTRS + ('data.$schema',)
        self._test_missing_required_sections(properties_to_remove)

    def test_document_missing_required_sections(self):
        self._read_data('sample_document')
        properties_to_remove = self.BASIC_ATTRS + (
            'metadata.substitutions',
            'metadata.substitutions.0.dest',
            'metadata.substitutions.0.dest.path',
            'metadata.substitutions.0.src',
            'metadata.substitutions.0.src.schema',
            'metadata.substitutions.0.src.name',
            'metadata.substitutions.0.src.path')
        self._test_missing_required_sections(properties_to_remove)

    def test_layering_policy_missing_required_sections(self):
        self._read_data('sample_layering_policy')
        properties_to_remove = self.BASIC_ATTRS + ('data.layerOrder',)
        self._test_missing_required_sections(properties_to_remove)

    def test_passphrase_missing_required_sections(self):
        self._read_data('sample_passphrase')
        properties_to_remove = self.BASIC_ATTRS + ('metadata.storagePolicy',)
        self._test_missing_required_sections(properties_to_remove)

    def test_passphrase_with_incorrect_storage_policy(self):
        self._read_data('sample_passphrase')
        expected_err = (
            "The provided deckhand/Passphrase/v1 YAML failed schema "
            "validation. Details: 'cleartext' does not match '^(encrypted)$'")
        wrong_data = self._corrupt_data('metadata.storagePolicy', 'cleartext',
                                        op='replace')

        e = self.assertRaises(errors.InvalidDocumentFormat,
                              document_validation.DocumentValidation,
                              wrong_data)
        self.assertIn(expected_err, str(e))

    def test_validation_policy_missing_required_sections(self):
        self._read_data('sample_validation_policy')
        properties_to_remove = self.BASIC_ATTRS + (
            'data.validations', 'data.validations.0.name')
        self._test_missing_required_sections(properties_to_remove)