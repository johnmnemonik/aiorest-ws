# -*- coding: utf-8 -*-
import unittest

from aiorest_ws.wrappers import Request, Response


class RequestTestCase(unittest.TestCase):

    def test_method_property(self):
        data = {}
        request = Request(**data)
        self.assertEqual(request.method, None)

    def test_method_property_2(self):
        data = {'method': None}
        request = Request(**data)
        self.assertEqual(request.method, None)

    def test_method_property_3(self):
        data = {'method': 'get'}
        request = Request(**data)
        self.assertEqual(request.method, 'get')

    def test_url_property(self):
        data = {}
        request = Request(**data)
        self.assertEqual(request.url, None)

    def test_url_property_2(self):
        data = {'url': None}
        request = Request(**data)
        self.assertEqual(request.url, None)

    def test_url_property_3(self):
        data = {'url': '/api'}
        request = Request(**data)
        self.assertEqual(request.url, '/api')

    def test_args_property(self):
        data = {}
        request = Request(**data)
        self.assertEqual(request.args, {})

    def test_args_property_2(self):
        data = {'args': None}
        request = Request(**data)
        self.assertEqual(request.args, None)

    def test_args_property_3(self):
        data = {'args': {'key': 'value'}}
        request = Request(**data)
        self.assertEqual(request.args, {'key': 'value'})

    def test_token_property(self):
        data = {}
        request = Request(**data)
        self.assertEqual(request.token, None)

    def test_token_property_2(self):
        data = {'token': None}
        request = Request(**data)
        self.assertEqual(request.token, None)

    def test_token_property_3(self):
        data = {'token': 'secret_token'}
        request = Request(**data)
        self.assertEqual(request.token, 'secret_token')

    def test_to_representation(self):
        data = {}
        request = Request(**data)
        self.assertEqual(
            request.to_representation(),
            {'method': None, 'url': None}
        )

    def test_to_representation_2(self):
        data = {'url': '/api'}
        request = Request(**data)
        self.assertEqual(
            request.to_representation(),
            {'method': None, 'url': '/api'}
        )

    def test_to_representation_3(self):
        data = {'method': 'GET'}
        request = Request(**data)
        self.assertEqual(
            request.to_representation(),
            {'method': 'GET', 'url': None}
        )

    def test_to_representation_4(self):
        data = {'url': '/api', 'method': 'GET'}
        request = Request(**data)
        self.assertEqual(
            request.to_representation(),
            {'method': 'GET', 'url': '/api', }
        )


class ResponseTestCase(unittest.TestCase):

    def test_init(self):
        response = Response()
        self.assertEqual(response._content, {})

    def test_content_getter(self):
        response = Response()
        self.assertEqual(response.content, {})

    def test_content_getter_2(self):
        response = Response()
        response._content = data = {'key': 'value'}
        self.assertEqual(response.content, data)

    def test_content_setter(self):
        response = Response()
        self.assertEqual(response.content, {})

    def test_content_setter_2(self):
        response = Response()
        response.content = data = {'details': 'some error'}
        self.assertEqual(response._content, data)

    def test_content_setter_3(self):
        response = Response()
        response.content = data = {'key': 'value'}
        self.assertEqual(response._content['data'], data)

    def test_content_setter_4(self):
        response = Response()
        response.content = data = [1, 2, 3, 4, 5]
        self.assertEqual(response._content['data'], data)

    def test_append_request(self):
        data = {'url': '/api', 'method': 'GET'}
        request = Request(**data)
        response = Response()
        response.append_request(request)
        self.assertEqual(
            response.content['request'], request.to_representation()
        )
