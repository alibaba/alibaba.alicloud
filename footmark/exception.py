
"""
Exception classes - Subclassing allows you to check for specific errors
"""
import base64
import xml.sax

import footmark

import json

StandardError = Exception

class FootmarkClientError(StandardError):
    """
    General Footmark Client error (error accessing AWS)
    """
    def __init__(self, reason, *args):
        super(FootmarkClientError, self).__init__(reason, *args)
        self.reason = reason

    def __repr__(self):
        return 'FootmarkClientError: %s' % self.reason

    def __str__(self):
        return 'FootmarkClientError: %s' % self.reason

class FootmarkServerError(StandardError):
    def __init__(self, status, body=None, *args):
        super(FootmarkServerError, self).__init__(status, body, *args)
        self.status = status
        # self.reason = reason
        self.body = body or ''
        self.request_id = None
        self.error_code = None
        self.message = ''
        self.host_id = None
        if isinstance(self.body, bytes):
            try:
                self.body = self.body.decode('utf-8')
            except UnicodeDecodeError:
                footmark.log.debug('Unable to decode body from bytes!')

        # Attempt to parse the error response. If body isn't present,
        # then just ignore the error response.
        if self.body:
            # Check if it looks like a ``dict``.
            if hasattr(self.body, 'items'):
                # It's not a string, so trying to parse it will fail.
                # But since it's data, we can work with that.
                self.request_id = self.body.get('RequestId', None)

                if 'Error' in self.body:
                    # XML-style
                    error = self.body.get('Error', {})
                    self.error_code = error.get('Code', None)
                    self.message = error.get('Message', None)
                else:
                    # JSON-style.
                    self.message = self.body.get('message', None)
            else:
                try:
                    parsed = json.loads(self.body)

                    if 'Error' in parsed:
                        if 'RequestId' in parsed:
                            self.request_id = parsed['RequestId']
                        if 'Code' in parsed['Error']:
                            self.error_code = parsed['Error']['Code']
                        if 'Message' in parsed['Error']:
                            self.message = parsed['Error']['Message']

                except (TypeError, ValueError):
                    # Remove unparsable message body so we don't include garbage
                    # in exception. But first, save self.body in self.error_message
                    # because occasionally we get error messages from Eucalyptus
                    # that are just text strings that we want to preserve.
                    self.message = self.body
                    self.body = None

    def __getattr__(self, name):
        if name == 'error_message':
            return self.message
        if name == 'code':
            return self.error_code
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'error_message':
            self.message = value
        else:
            super(FootmarkServerError, self).__setattr__(name, value)

    def __repr__(self):
        return '%s: %s %s\n%s' % (self.__class__.__name__,
                                  self.status, self.message, self.body)

    def __str__(self):
        return '%s: %s %s\n%s' % (self.__class__.__name__,
                                  self.status, self.message, self.body)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name in ('RequestId', 'RequestID'):
            self.request_id = value
        elif name == 'Code':
            self.error_code = value
        elif name == 'Message':
            self.message = value
        elif name == 'HostId':
            self.host_id = value
        return None

    def _cleanupParsedProperties(self):
        self.request_id = None
        self.error_code = None
        self.message = None
        self.box_usage = None


class ConsoleOutput(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.instance_id = None
        self.timestamp = None
        self.comment = None
        self.output = None

    def startElement(self, name, attrs, connection):
        return None

    def endElement(self, name, value, connection):
        if name == 'instanceId':
            self.instance_id = value
        elif name == 'output':
            self.output = base64.b64decode(value)
        else:
            setattr(self, name, value)


class ECSResponseError(FootmarkServerError):
    """
    Error in response from ECS.
    """
    def __init__(self, status, reason, body=None):
        self.errors = None
        self._errorResultSet = []
        super(ECSResponseError, self).__init__(status, reason, body)
        self.errors = [
            (e.error_code, e.error_message) for e in self._errorResultSet]
        if len(self.errors):
            self.error_code, self.error_message = self.errors[0]

    def startElement(self, name, attrs, connection):
        if name == 'Errors':
            self._errorResultSet = ResultSet([('Error', _ECSError)])
            return self._errorResultSet
        else:
            return None

    def endElement(self, name, value, connection):
        if name == 'RequestID':
            self.request_id = value
        else:
            return None  # don't call subclass here

    def _cleanupParsedProperties(self):
        super(ECSResponseError, self)._cleanupParsedProperties()
        self._errorResultSet = []
        for p in ('errors'):
            setattr(self, p, None)


class JSONResponseError(FootmarkServerError):
    """
    This exception expects the fully parsed and decoded JSON response
    body to be passed as the body parameter.

    :ivar status: The HTTP status code.
    :ivar reason: The HTTP reason message.
    :ivar body: The Python dict that represents the decoded JSON
        response body.
    :ivar error_message: The full description of the AWS error encountered.
    :ivar error_code: A short string that identifies the AWS error
        (e.g. ConditionalCheckFailedException)
    """
    def __init__(self, status, reason, body=None, *args):
        self.status = status
        self.reason = reason
        self.body = body
        if self.body:
            self.error_message = self.body.get('message', None)
            self.error_code = self.body.get('__type', None)
            if self.error_code:
                self.error_code = self.error_code.split('#')[-1]


class _ECSError(object):
    def __init__(self, connection=None):
        self.connection = connection
        self.error_code = None
        self.error_message = None

    def startElement(self, name, attrs, connection):
        return None

    def endElement(self, name, value, connection):
        if name == 'Code':
            self.error_code = value
        elif name == 'Message':
            self.error_message = value
        else:
            return None

