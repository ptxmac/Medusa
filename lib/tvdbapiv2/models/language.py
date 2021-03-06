# coding: utf-8

"""
Copyright 2015 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems


class Language(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Language - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'int',
            'abbreviation': 'str',
            'name': 'str',
            'english_name': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'abbreviation': 'abbreviation',
            'name': 'name',
            'english_name': 'englishName'
        }

        self._id = None
        self._abbreviation = None
        self._name = None
        self._english_name = None

    @property
    def id(self):
        """
        Gets the id of this Language.


        :return: The id of this Language.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Language.


        :param id: The id of this Language.
        :type: int
        """
        self._id = id

    @property
    def abbreviation(self):
        """
        Gets the abbreviation of this Language.


        :return: The abbreviation of this Language.
        :rtype: str
        """
        return self._abbreviation

    @abbreviation.setter
    def abbreviation(self, abbreviation):
        """
        Sets the abbreviation of this Language.


        :param abbreviation: The abbreviation of this Language.
        :type: str
        """
        self._abbreviation = abbreviation

    @property
    def name(self):
        """
        Gets the name of this Language.


        :return: The name of this Language.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Language.


        :param name: The name of this Language.
        :type: str
        """
        self._name = name

    @property
    def english_name(self):
        """
        Gets the english_name of this Language.


        :return: The english_name of this Language.
        :rtype: str
        """
        return self._english_name

    @english_name.setter
    def english_name(self, english_name):
        """
        Sets the english_name of this Language.


        :param english_name: The english_name of this Language.
        :type: str
        """
        self._english_name = english_name

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other): 
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

