"""Google Compute Engine Instance."""

import requests

class GoogleComputeEngine(object):

    def __init__(self):
        self.server = "http://metadata/computeMetadata/v1/instance/"
        self.headers = {"Metadata-Flavor": "Google"}
        self._id = None
        self._name = None
        self._zone = None
        self._externalIp = None
        self._internalIp = None
        try:
            self._id = requests.get(self.server + "id", headers=self.headers).text
        except requests.exceptions.ConnectTimeout:
            self.is_instance = False
        else:
            self.is_instance = True


    def isInstance(self):
        return self.is_instance


    def instanceId(self):
        if not self.is_instance:
            return ''
        return self._id


    def instanceName(self):
        if not self.is_instance:
            return ''
        if self._name is None:
            self._name = requests.get(self.server + "hostname", headers=self.headers).text
        return self._name


    def instanceZone(self):
        if not self.is_instance:
            return ''
        if self._zone is None:
            self._zone = requests.get(self.server + "zone", headers=self.headers).text
        return self._zone


    def instanceExternalIP(self):
        if not self.is_instance:
            return ''
        if self._externalIp is None:
            self._externalIp = requests.get(self.server + "network-interfaces/0/access-configs/0/external-ip", headers=self.headers).text
        return self._externalIp


    def instanceInternalIP(self):
        if not self.is_instance:
            return ''
        if self._internalIp is None:
            self._internalIp = requests.get(self.server + "network-interfaces/0/ip", headers=self.headers).text
        return self._internalIp
