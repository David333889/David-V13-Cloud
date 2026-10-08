"""Cross-contract rejection cases for otherwise complete synthetic packets."""
import copy
import unittest

from research.test_wp4_corporate_action_factor_evidence import packet as c06_packet, formula
from research.test_wp4_historical_asof_revision_evidence import fully_supported_packet
from research.test_wp4_reinvestment_economic_equivalence_evidence import packet as c07_packet, supported_claim
from research.wp4_corporate_action_factor_evidence import assess_c06_evidence
from research.wp4_historical_asof_revision_evidence import assess_c10_evidence
from research.wp4_reinvestment_economic_equivalence_evidence import assess_c07_c12_evidence


def complete_candidates():
    c06 = c06_packet()
    c06['formula_evidence'] = formula('SUPPORTED')
    c06['formula_authentication_complete'] = True
    c07 = c07_packet()
    for section in ('reinvestment_evidence', 'equivalence_evidence'):
        c07[section] = {name: supported_claim() for name in c07[section]}
    c07['reinvestment_authentication_complete'] = True
    c07['equivalence_authentication_complete'] = True
    return (
        (assess_c06_evidence, c06, ('formula_verified',)),
        (assess_c07_c12_evidence, c07, ('reinvestment_verified', 'economic_equivalence_verified')),
        (assess_c10_evidence, fully_supported_packet(), ('historical_asof_verified', 'revision_provenance_verified', 'point_in_time_verified', 'lookahead_safe')),
    )


class DeclarationSafetyTests(unittest.TestCase):
    def assert_safety(self, result):
        self.assertTrue(result['research_only'])
        self.assertFalse(result['source_verified'])
        self.assertFalse(result['production_eligible'])
        self.assertEqual(result['execution_readiness'], 'BLOCKED')

    def test_invalid_declaration_never_verifies_complete_packet(self):
        for assess, packet, flags in complete_candidates():
            for value in (False, None, 1, 'True', [], {}):
                with self.subTest(contract=assess.__name__, value=value):
                    candidate = copy.deepcopy(packet)
                    candidate['synthetic_only'] = value
                    before = copy.deepcopy(candidate)
                    result = assess(candidate)
                    self.assertIn('RESEARCH_DECLARATION_REQUIRED', result['issues'])
                    for flag in flags:
                        self.assertFalse(result[flag], flag)
                    self.assert_safety(result)
                    self.assertEqual(candidate, before)

    def test_missing_declaration_never_verifies_complete_packet(self):
        for assess, packet, flags in complete_candidates():
            with self.subTest(contract=assess.__name__):
                del packet['synthetic_only']
                result = assess(packet)
                for flag in flags:
                    self.assertFalse(result[flag], flag)
                self.assert_safety(result)

    def test_supported_synthetic_packets_keep_research_only_behavior(self):
        for assess, packet, flags in complete_candidates():
            result = assess(packet)
            for flag in flags:
                self.assertTrue(result[flag], flag)
            self.assert_safety(result)

    def test_malformed_events_return_issue_instead_of_throwing(self):
        for events in ([{}], [[]], [None], [1], ['UNKNOWN'], [], None, 'STOCK_SPLIT'):
            with self.subTest(events=events):
                candidate = complete_candidates()[0][1]
                candidate['framework']['event_types'] = events
                before = copy.deepcopy(candidate)
                result = assess_c06_evidence(candidate)
                self.assertIn('EVENT_TAXONOMY_EVIDENCE_REQUIRED', result['issues'])
                self.assertFalse(result['framework_supported'])
                self.assertFalse(result['formula_verified'])
                self.assert_safety(result)
                self.assertEqual(candidate, before)

    def test_unsupported_provider_capabilities_cannot_pass_c10(self):
        candidate = fully_supported_packet()
        for name in candidate['historical_evidence']:
            candidate['historical_evidence'][name]['state'] = (
                'PARTIAL' if name == 'correction_history' else 'UNSUPPORTED_REPORTED'
            )
        result = assess_c10_evidence(candidate)
        self.assertFalse(result['historical_asof_verified'])
        self.assertFalse(result['lookahead_safe'])
        self.assert_safety(result)


if __name__ == '__main__':
    unittest.main()
