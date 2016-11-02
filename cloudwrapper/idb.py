"""
Influx DB direct use (as SQL database).

Copyright (C) 2016 Klokan Technologies GmbH (http://www.klokantech.com/)
Author: Martin Mikita <martin.mikita@klokantech.com>
"""

import json
import errno
import datetime
import socket

from time import sleep

try:
    from influxdb import InfluxDBClient
except ImportError:
    from warnings import warn
    install_modules = [
        'influxdb==3.0.0',
    ]
    warn('cloudwrapper.idl requires these packages:\n  - {}'.format('\n  - '.join(install_modules)))
    raise


class IdbConnection(object):

    def __init__(self, user, pswd, host='localhost', port=8086, db='static'):
        self.host = host
        self.port = int(port)
        self.client = InfluxDBClient(self.host, self.port, user, pswd, db)
        self.client.create_database(db)
        self.client.switch_database(db)


    def table(self, name, tags=None):
        """
        Return Table object, tags is list of columns that should be indexed
        """
        return Handler(self.client, name, tags)



class Table(object):

    def __init__(self, client, name, tags):
        """
        Create Table object with name, using client connection.
        """
        self.name = name
        self.client = client
        self.tags = tags


    def logId(self):
        return self.logId


    def insert(self, data):
        """
        Insert data into this table
        """
        tagsData = {}
        fieldsData = {}
        # Separate tags from other values - fields
        if not isinstance(data, dict):
            raise Error('Invalid format of data, expected dict')
        for col in data:
            val = data[col]
            if not isinstance(val, (str, unicode)):
                val = json.dumps(val, separators=(',', ':'))
            if col in self.tags:
                tagsData[col] = val
            else:
                fieldsData[col] = val
        points = [{
            'measurement': self.name,
            'fields': fieldsData,
            'tags': tagsData,
        }]
        try:
            return self.client.write_points(points)
        except Exception as e:
            raise Exception('Unable to insert data into this table: '+str(e))


    def get(self, col, value):
        sql = 'SELECT * FROM "{}" WHERE "{}" = \'{}\''.format(self.name, col, value)
        rs = client.query(sql)
        return list(rs.get_points())


    def list(self, columns=None):

        sql = 'SELECT '
        sqlCols = []
        for col in columns:
            sqlcols.append('"{}"'.format(col))
        if not sqlCols:
            sqlCols.append('*')
        sql += ','.join(sqlCols)

        sql += 'FROM "{}"'.format(self.name)

        # filter and orderAsc is not implemented yet
        rs = client.query(sql)
        if rs:
            for row in rs:
                yield row
