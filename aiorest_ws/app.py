# -*- coding: utf-8 -*-
"""
    This module implements the central application object.
"""
__all__ = ('Application', )

import asyncio

from time import gmtime, strftime

from .__init__ import __version__
from .server import RestWSServerFactory, RestWSServerProtocol
from .validators import validate_subclass


class Application(object):
    """Main application of aiorest-ws framework."""
    # TODO: Add logger
    # TODO: Add compressing messages
    # TODO: Add SSL support

    _factory = RestWSServerFactory
    _protocol = RestWSServerProtocol
    _certificate = None
    _key = None

    def __init__(self, *args, **options):
        """Initialization of Application instance."""
        super(Application, self).__init__()
        self.factory = options.get('factory')
        self.protocol = options.get('protocol')
        self.certificate = options.get('certificate')
        self.key = options.get('key')

    @property
    def factory(self):
        return self._factory

    @factory.setter
    def factory(self, factory):
        if factory:
            validate_subclass(self, '_factory', factory, RestWSServerFactory)

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        if protocol:
            validate_subclass(self, '_protocol', protocol,
                              RestWSServerProtocol)

    @property
    def certificate(self):
        return self._certificate

    @certificate.setter
    def certificate(self, certificate):
        self._certificate = certificate

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def url(self):
        if self.certificate and self.key:
            url = "wss://{0}:{1}"
        else:
            url = "ws://{0}:{1}"
        return url

    def create_factory(self, url, **options):
        """Create a factory instance."""
        debug = options.get('debug', False)
        router = options.get('router')

        factory = self.factory(url, debug=debug)
        factory.protocol = self.protocol

        if router:
            factory.router = router

        return factory

    def generate_url(self, host, port):
        """Generate URL to application."""
        return self.url.format(host, port)

    def run(self, host='127.0.0.1', port=8080, router=None, debug=False,
            **options):
        """Create and start web server with some IP and PORT.

        :param host: the hostname to listen on. Defaults to ``'127.0.0.1'``.
        :param port: the port of the server. Defaults to ``8080``.
        :param router: instance of AbstractRouter subclass.
        :param debug: enable or disable debug mode. By default debug mode
                      is disabled.
        :param options: other parameters, which can be used for configuration
                        of the Application.
        """
        url = self.generate_url(host, port)

        factory = self.create_factory(url, debug=debug, router=router,
                                      **options)

        loop = asyncio.get_event_loop()
        server_coroutine = loop.create_server(factory, host, port)
        server = loop.run_until_complete(server_coroutine)

        print(strftime("%d %b, %Y - %X", gmtime()))
        print("aiorest-ws version {0}".format(__version__))
        print("Server started at {0}".format(url))
        print("Quit the server with CONTROL-C.")

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.close()
            loop.close()