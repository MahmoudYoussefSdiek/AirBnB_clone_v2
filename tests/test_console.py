#!/usr/bin/python3
"""Unittest for console.py"""
import unittest
from unittest.mock import patch
from io import StringIO
import os
from console import HBNBCommand
from models import storage


class TestConsole(unittest.TestCase):
    """Test cases for the console"""

    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()

    def tearDown(self):
        """Tear down test environment"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_create(self):
        """Test create command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State')
            id = f.getvalue().strip()
        self.assertTrue(len(id) > 0)
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create')
            output = f.getvalue().strip()
        self.assertEqual(output, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create MyModel')
            output = f.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_show(self):
        """Test show command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State')
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('show State {}'.format(id))
            output = f.getvalue().strip()
        self.assertIn(id, output)
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('show State')
            output = f.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('show MyModel {}'.format(id))
            output = f.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('show State 12345')
            output = f.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_destroy(self):
        """Test destroy command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State')
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('destroy State {}'.format(id))
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('show State {}'.format(id))
            output = f.getvalue().strip()
        self.assertEqual(output, "** no instance found **")
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('destroy')
            output = f.getvalue().strip()
        self.assertEqual(output, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('destroy MyModel {}'.format(id))
            output = f.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('destroy State 12345')
            output = f.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_all(self):
        """Test all command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State')
            id1 = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create City')
            id2 = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('all')
            output = f.getvalue().strip()
        self.assertIn(id1, output)
        self.assertIn(id2, output)
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('all MyModel')
            output = f.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_update(self):
        """Test update command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State')
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('update State {} name "California"'.format(id))
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('show State {}'.format(id))
            output = f.getvalue().strip()
        self.assertIn('California', output)
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('update')
            output = f.getvalue().strip()
        self.assertEqual(output, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('update MyModel {}'.format(id))
            output = f.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('update State')
            output = f.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('update State 12345')
            output = f.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_create_with_params(self):
        """Test create command with parameters"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California"')
            id1 = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="Arizona"')
            id2 = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 latitude=37.773972 longitude=-122.431297')
            id3 = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('all State')
            output = f.getvalue().strip()
        self.assertIn('California', output)
        self.assertIn('Arizona', output)
        self.assertIn(id1, output)
        self.assertIn(id2, output)
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('all Place')
            output = f.getvalue().strip()
        self.assertIn('My little house', output)
        self.assertIn(id3, output)

    def test_count(self):
        """Test count command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State')
            id1 = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State')
            id2 = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create City')
            id3 = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('count State')
            output = f.getvalue().strip()
        self.assertEqual(output, '2')
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('count City')
            output = f.getvalue().strip()
        self.assertEqual(output, '1')
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('count MyModel')
            output = f.getvalue().strip()
        self.assertEqual(output, '0')

    def test_quit(self):
        """Test quit command"""
        with self.assertRaises(SystemExit):
            self.console.onecmd('quit')

    def test_EOF(self):
        """Test EOF command"""
        with self.assertRaises(SystemExit):
            self.console.onecmd('EOF')

    def test_help(self):
        """Test help command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('help')
            output = f.getvalue().strip()
        self.assertTrue(len(output) > 0)
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('help create')
            output = f.getvalue().strip()
        self.assertTrue(len(output) > 0)
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('help MyModel')
            output = f.getvalue().strip()
        self.assertEqual(output, "** No help on MyModel **")

    def test_emptyline(self):
        """Test empty line"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('')
            output = f.getvalue().strip()
        self.assertEqual(output, '')

if __name__ == '__main__':
    unittest.main()
