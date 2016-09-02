"""
Handles basic connections to ACS
"""

import xml.sax
import six
import footmark
import importlib
from footmark.exception import FootmarkServerError
from footmark.provider import Provider
import json

from aliyunsdkcore import client

class ACSAuthConnection(object):
    def __init__(self, acs_access_key_id=None,
                 acs_secret_access_key=None,
                 region=None,
                 provider='acs', security_token=None):
        """
        :keyword str acs_access_key_id: Your ACS Access Key ID (provided by
            Alicloud). If none is specified, the value in your
            ``ACS_ACCESS_KEY_ID`` environmental variable is used.
        :keyword str acs_secret_access_key: Your ACS Secret Access Key
            (provided by Alicloud). If none is specified, the value in your
            ``ACS_SECRET_ACCESS_KEY`` environmental variable is used.
        :keyword str security_token: The security token associated with
            temporary credentials issued by STS.  Optional unless using
            temporary credentials.  If none is specified, the environment
            variable ``ACS_SECURITY_TOKEN`` is used if defined.

        :keyword str region: The region ID.

        """
        self.region = region
        if isinstance(provider, Provider):
            # Allow overriding Provider
            self.provider = provider
        else:
            self._provider_type = provider
            self.provider = Provider(self._provider_type,
                                     acs_access_key_id,
                                     acs_secret_access_key,
                                     security_token)

    def acs_access_key_id(self):
        return self.provider.access_key
    acs_access_key_id = property(acs_access_key_id)
    access_key = acs_access_key_id

    def acs_secret_access_key(self):
        return self.provider.secret_key
    acs_secret_access_key = property(acs_secret_access_key)
    secret_key = acs_secret_access_key

    def region_id(self):
        return self.region

class ACSQueryConnection(ACSAuthConnection):

    ResponseError = FootmarkServerError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, product=None, security_token=None, provider='acs'):
        super(ACSQueryConnection, self).__init__(
            acs_access_key_id,
            acs_secret_access_key,
            region=region,
            security_token=security_token,
            provider=provider)

        self.product = product

    def make_request(self, action, params=None):
        conn = client.AcsClient(self.acs_access_key_id, self.acs_secret_access_key, self.region)
        if action:
            module = importlib.import_module(self.product + '.' + action + 'Request')
            request = getattr(module, action + 'Request')()
            request.set_accept_format('json')
            if params and isinstance(params, dict):
                for k,v in params.items():
                    getattr(request, k)(v)
        return conn.get_response(request)

    def build_list_params(self, params, items, label):
        params['set_%s' % label] = items

    def parse_response(self, markers, response):
        results = []
        response = json.loads(response, 'UTF-8')
        if markers[0] in response:
            for value in response[markers[0]].itervalues():
                if value is None or len(value)<1:
                    return results
                for item in value:
                    element = markers[1]
                    self.parse_dict(element, item)
                    results.append(element)
        return results

    def parse_dict(self, element, dict_data):
        if isinstance(dict_data, dict):
            for k,v in dict_data.items():
                if isinstance(v, dict):
                    value = {}
                    for kk,vv in v.items():
                        value[self.convert_name(kk)] = vv
                    v = value
                    self.parse_dict(element, v)
                setattr(element, self.convert_name(k), v)

    def convert_name(self, name):
        if not name:
            return None
        new_name = ''
        for ch in name:
            if ch.isupper():
                ch = '_' + ch.lower()
            new_name += ch
        if new_name.startswith('_'):
            new_name = new_name[1:]
        return new_name
    # generics

    def get_list(self, action, params, markers, parent=None):
        if not parent:
            parent = self
        response = self.make_request(action, params)
        body = response[-1]
        footmark.log.debug(body)
        print 'body:', body
        if not body:
            footmark.log.error('Null body %s' % body)
            raise self.ResponseError(response[0], body)
        elif response[0] in (200, 201):
            return self.parse_response(markers, body)
        else:
            footmark.log.error('%s %s' % (response[0], body))
            raise self.ResponseError(response[0], body)

    def get_object(self, action, params, cls, parent=None):
        if not parent:
            parent = self
        response = self.make_request(action, params)
        body = response[-1]
        footmark.log.debug(body)
        if not body:
            footmark.log.error('Null body %s' % body)
            raise self.ResponseError(response.status, response.reason, body)
        elif response[0] == 200:
            obj = cls(parent)
            h = footmark.handler.XmlHandler(obj, parent)
            if isinstance(body, six.text_type):
                body = body.encode('utf-8')
            xml.sax.parseString(body, h)
            return obj
        else:
            footmark.log.error('%s %s' % (response.status, response.reason))
            footmark.log.error('%s' % body)
            raise self.ResponseError(response.status, response.reason, body)

