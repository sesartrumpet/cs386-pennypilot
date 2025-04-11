# -*- coding: utf-8 -*-

# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2009, 2013, Oracle and/or its affiliates. All rights reserved.

# MySQL Connector/Python is licensed under the terms of the GPLv2
# <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most
# MySQL Connectors. There are special exceptions to the terms and
# conditions of the GPLv2 as it is applied to this software, see the
# FOSS License Exception
# <http://www.mysql.com/about/legal/licensing/foss-exception.html>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

"""
Configuration module for the PennyPilot application.
This module contains all the necessary configuration settings for the application,
including database connection parameters and other system-wide settings.
"""

class Config(object):
    """
    Configuration class that holds all settings for the PennyPilot application.
    This class uses class-level variables to store configuration that can be
    accessed throughout the application.
    
    To modify these settings:
    1. Change the values below to match your environment
    2. Ensure the database exists and is accessible
    3. Verify the user has proper permissions
    """

    # Database connection settings
    HOST = 'localhost'      # MySQL server host address
    DATABASE = 'pennypilot_db'  # Name of the database to use
    USER = 'root'      # MySQL username
    PASSWORD = '123455'  # MySQL password
    PORT = 3306    # MySQL server port
    
    # Character encoding settings
    CHARSET = 'utf8'    # Character set for database connection
    UNICODE = True      # Whether to use Unicode
    
    # Debug settings
    WARNINGS = True     # Whether to show MySQL warnings

    @classmethod
    def dbinfo(cls):
        """
        Returns a dictionary containing all database connection parameters.
        This method is used to create database connections throughout the application.
        
        Returns:
            dict: A dictionary containing all database connection parameters
        """
        return {
            'host': cls.HOST,
            'database': cls.DATABASE,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'charset': cls.CHARSET,
            'use_unicode': cls.UNICODE,
            'get_warnings': cls.WARNINGS,
            'port': cls.PORT,
        }
