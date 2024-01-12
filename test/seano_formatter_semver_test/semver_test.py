import unittest
from seano_cli.utils import SeanoFatalError
from seano_formatter_semver.semver import recalculate_current_semver


class HlistParsingTests(unittest.TestCase):
    def testPathological(self):
        self.assertRaises(SeanoFatalError, lambda: recalculate_current_semver(None))
        self.assertRaises(SeanoFatalError, lambda: recalculate_current_semver({}))
        self.assertRaises(SeanoFatalError, lambda: recalculate_current_semver({'releases': None}))
        self.assertRaises(SeanoFatalError, lambda: recalculate_current_semver({'releases': []}))


    def testEmptyProject(self):
        self.assertEqual('0.0.1', recalculate_current_semver({'releases': [{
        }]}))


    def testNewProject(self):
        self.assertEqual('0.0.1', recalculate_current_semver({'releases': [{'notes':[{
            'anything': 0,
        }]}]}))
        self.assertEqual('0.1.0', recalculate_current_semver({'releases': [{'notes':[{
            'features': 0,
        }]}]}))
        self.assertEqual('1.0.0', recalculate_current_semver({'releases': [{'notes':[{
            'upgrade': 0,
        }]}]}))


    def testExistingProject(self):
        self.assertEqual('1.2.4', recalculate_current_semver({'releases': [{
            'after': [{'name': '1.2.3'},
                      {'name': '2.3.4', 'is-backstory': True}],
            'notes': [{
                'anything': 0,
            }],
        }]}))
        self.assertEqual('1.3.0', recalculate_current_semver({'releases': [{
            'after': [{'name': '1.2.3'},
                      {'name': '2.3.4', 'is-backstory': True}],
            'notes': [{
                'features': 0,
            }],
        }]}))
        self.assertEqual('2.0.0', recalculate_current_semver({'releases': [{
            'after': [{'name': '1.2.3'},
                      {'name': '2.3.4', 'is-backstory': True}],
            'notes': [{
                'upgrade': 0,
            }],
        }]}))


if __name__ == '__main__':
    unittest.main()
