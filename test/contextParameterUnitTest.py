import unittest
import sys

sys.path.append('../src/')

from contextParameter import ContextParameter

# How to run, execute from test dir:
# python -m contextParameterUnitTest
class ContextParameterUnitTest(unittest.TestCase):
    def test_contextChanges(self):
        uut = ContextParameter()
        # Double check
        uut.SetState('a', 'b', 0.1, 0.2)
        self.assertTrue(uut.HasAnyChanged())
        self.assertTrue(uut.HasAnyChanged())

        # Nothing change
        uut.SetState('a', 'b', 0.3, 0.2)
        self.assertTrue(uut.HasAnyChanged())
        uut.SetState('a', 'b', 0.3, 0.2)
        self.assertFalse(uut.HasAnyChanged())

        # Date change
        uut.SetState('ab', 'b', 0.1, 0.2)
        self.assertTrue(uut.HasAnyChanged())
        uut.SetState('ab', 'b', 0.1, 0.2)
        self.assertFalse(uut.HasAnyChanged())

        # Shift change
        uut.SetState('ab', 'ab', 0.1, 0.2)
        self.assertTrue(uut.HasAnyChanged())
        uut.SetState('ab', 'ab', 0.1, 0.2)
        self.assertFalse(uut.HasAnyChanged())

        # Corr threshold change
        uut.SetState('ab', 'ab', 0.11, 0.2)
        self.assertTrue(uut.HasAnyChanged())
        uut.SetState('ab', 'ab', 0.11, 0.2)
        self.assertFalse(uut.HasAnyChanged())

        # Corr Value change
        uut.SetState('ab', 'ab', 0.11, 0.22)
        self.assertTrue(uut.HasAnyChanged())
        uut.SetState('ab', 'ab', 0.11, 0.22)
        self.assertFalse(uut.HasAnyChanged())

if __name__ == '__main__':
    unittest.main()