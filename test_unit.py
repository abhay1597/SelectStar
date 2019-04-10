# -*- coding: utf-8 -*

import io
import sys,re
import unittest
from ln2sql import main as ln2sql_main
from ParsingException import ParsingException


class SimplisticTest(unittest.TestCase):

    def _cleanOutput(self, s):
        s = s.split("SELECT")[1]        # remove table schema
        s = re.sub("\\033.*?m", "", s)  # remove color codes
        s = s.replace('\n',' ')         # remove '\n'
        s = s.split(';')[0]             # remove spaces after ;
        s = "SELECT" + s + ';'          # put back lost SELECT and ';'
        return s

    def test_main(self):
        correctTest = [
            {
                'input': 'List me the info of city table',
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': 'SELECT * FROM city;'
            },
            {
                'input': 'What is the number of the city in this database?',
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': 'SELECT COUNT(*) FROM city;'
            },
            {
                'input': 'Tell me all id from city',
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': 'SELECT city.id FROM city;'
            },
            {
                'input': 'What are the name of emp',
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': 'SELECT emp.name FROM emp;'
            },
            {
                'input': 'List all name and score of all emp',
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': 'SELECT emp.name, emp.score FROM emp;'
            },
            {
                'input': 'Count how many city there are where the name is Matthew ?',
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId WHERE emp.name = 'matthew';"
            },
            {
                'input': 'What is the emp with the name is rupinder ?',
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': "SELECT * FROM emp WHERE emp.name = 'rupinder';"
            },
            {
                'input': 'What is the cityName and the score of the emp whose name is matthew',
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': "SELECT city.cityName, emp.score FROM emp INNER JOIN city ON emp.cityId = city.id WHERE emp.name = 'matthew';"
            },
            {
                'input': 'Count how many city there are where the score is greater than 2 ?',
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId WHERE emp.score > '2';"
            },
            {
                'input': "Show data for city where cityName is 'Pune Agra'",
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': "SELECT * FROM city WHERE city.cityName = 'pune agra';"
            },
            {
                'input': "Show data for city where cityName is not Pune and id like 1",
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': "SELECT * FROM city WHERE city.cityName != 'pune' AND city.id LIKE '%1%';"
            },
            {
                'input': "What is the cityName and the score of the emp whose name is rupinder",
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': "SELECT city.cityName, emp.score FROM emp INNER JOIN city ON emp.cityId = city.id WHERE emp.name = 'rupinder';"
            },
            {
                'input': "count how many city there are ordered by name",
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name ASC;"
            },
            {
                'input': "count how many city there are ordered by name in descending order and ordered by score in ascending order",
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name DESC, emp.score ASC;"
            },
            {
                'input': "count how many city there are ordered by name in descending order and ordered by score?",
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name DESC, emp.score ASC;"
            },
            {
                'input': "count distinctly how many city there are ordered by name in descending and ordered by score?",
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name DESC, emp.score ASC;"
            },
            {
                'input': "Count distinctly how many different name of city there are ordered by name in descending and ordered by score?",
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': "SELECT COUNT(DISTINCT emp.name) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name DESC, emp.score ASC;"
            },
            {
                'input': "What are the distinct name of city with a score equals to 9?",
                'database': './database/city.sql',
                'language': './lang/english.csv',
                'output': "SELECT DISTINCT emp.name FROM city INNER JOIN emp ON city.id = emp.cityId WHERE emp.score = '9';"
            }
        ]

        for test in correctTest:
            capturedOutput = io.StringIO()
            sys.stdout = capturedOutput
            ln2sql_main(['-d', test['database'], '-l', test['language'], '-i', test['input']])
            sys.stdout = sys.__stdout__
            self.assertEqual(self._cleanOutput(capturedOutput.getvalue()), test['output'])



class ThesaurusTest(unittest.TestCase):

    def _cleanOutput(self, s):
        s = s.split("SELECT")[1]        # remove table schema
        s = re.sub("\\033.*?m", "", s)  # remove color codes
        s = s.replace('\n',' ')         # remove '\n'
        s = s.split(';')[0]             # remove spaces after ;
        s = "SELECT" + s + ';'          # put back lost SELECT and ';'
        return s

    def test_main(self):
        for test in thesaurusTest:
            capturedOutput = io.StringIO()
            sys.stdout = capturedOutput
            ln2sql_main(['-d', test['database'], '-l', test['language'], '-i', test['input'], '-t', test['thesaurus']])
            sys.stdout = sys.__stdout__
            self.assertEqual(self._cleanOutput(capturedOutput.getvalue()), test['output'])

class ExceptionTest(unittest.TestCase):

    def test_main(self):
        for test in errorTest:
            self.assertRaises(Exception, ln2sql_main, ['-d', test['database'], '-l', test['language'], '-i', test['input']])

if __name__ == '__main__':
    unittest.main()
