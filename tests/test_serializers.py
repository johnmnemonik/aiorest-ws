import unittest

from aiorest_ws.exceptions import NotImplementedMethod, SerializerError
from aiorest_ws.serializers import BaseSerializer, JSONSerializer, \
    XMLSerializer


class TestBaseSerializer(unittest.TestCase):

    def setUp(self):
        super(TestBaseSerializer, self).setUp()
        self.bs = BaseSerializer()

    def test_fail_serialize(self):
        self.assertRaises(NotImplementedMethod, self.bs.serialize, {})


class TestJSONSerializer(unittest.TestCase):

    def setUp(self):
        super(TestJSONSerializer, self).setUp()
        self.json = JSONSerializer()

    def test_serialize_invalid_data(self):
        self.assertRaises(SerializerError, self.json.serialize, object)

    def test_using_short_separators(self):
        self.json.compact = True
        data = {'objects': [1, 2, 3]}
        output = self.json.serialize(data)
        self.assertEqual(output, b'{"objects":[1,2,3]}')

    def test_using_long_separators(self):
        self.json.compact = False
        data = {'objects': [1, 2, 3]}
        output = self.json.serialize(data)
        self.assertEqual(output, b'{"objects": [1, 2, 3]}')

    def test_ensure_ascii_is_true(self):
        self.json.ensure_ascii = True
        data = {"last_name": u"王"}
        output = self.json.serialize(data)
        self.assertEqual(output, b'{"last_name": "\\u738b"}')

    def test_ensure_ascii_is_false(self):
        self.json.ensure_ascii = False
        data = {"last_name": u"王"}
        output = self.json.serialize(data)
        self.assertEqual(output, b'{"last_name": "\xe7\x8e\x8b"}')

    def test_bad_unicode_symbols(self):
        data = ["\u2028", "\u2029"]
        output = self.json.serialize(data)
        self.assertEqual(output, b'["\\u2028", "\\u2029"]')


class TestXMLSerializer(unittest.TestCase):

    def setUp(self):
        super(TestXMLSerializer, self).setUp()
        self.xml = XMLSerializer()

    def test_serialize_invalid_data(self):
        self.assertRaises(SerializerError, self.xml.serialize, {None: 'test'})

    def test_valid_serialization(self):
        data = {'objects': [1, 2, 3]}
        output = self.xml.serialize(data)
        self.assertIn('<objects><list-item>1</list-item><list-item>2'
                      '</list-item>''<list-item>3</list-item></objects>',
                      output)
