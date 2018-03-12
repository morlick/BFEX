from bfex.components.search_engine.parser import QueryParser, QueryException
import pytest


class TestParser(object):
    parser = QueryParser()

    def test_parse_valid_query(self):
        # Simple one word query
        query = "query"
        result = self.parser.parse_query(query)
        assert len(result) == 1
        assert "query" in result[0][1]

        # Simple two term query with one operators
        query = "big AND bad"
        result = self.parser.parse_query(query)
        assert len(result) == 3
        assert result == [("KEYWORD", "big"), ("KEYWORD", "bad"), "AND"]

        # more complicated 3 term query
        query = "big AND ( bad OR bold )"
        result = self.parser.parse_query(query)
        assert len(result) == 5
        assert result == [('KEYWORD', 'big'), ('KEYWORD', 'bad'),
                                  ('KEYWORD', 'bold'), 'OR', 'AND']

        query = "( big AND bad ) OR ( bold AND bad )"
        result = self.parser.parse_query(query)
        assert len(result) == 7
        assert result == [('KEYWORD', 'big'), ('KEYWORD', 'bad'), 'AND',
                                  ('KEYWORD', 'bold'), ('KEYWORD', 'bad'), 'AND', 'OR']

        query = '"stemming should" OR "stemming increases"'
        result = self.parser.parse_query(query)
        assert result == [('PHRASE', ['stemming', 'should']),
                                ('PHRASE', ['stemming', 'increases']), 'OR']

    def test_invalid_queries(self):
        # Tests invalid queries that cant be processed.
        invalid_queries = ["AND buzz lightyear", "Buzz lightyear AND", "AND OR AND",
                          "()", '"phrase OR query"', "(woody AND buzz) Buzz",
                          "(woody AND buzz) AND AND", '"phrase ()"', "( Word AND word",
                          "term (OR term2 AND term3)", "AND"]

        for query in invalid_queries:
            with pytest.raises(QueryException):
                self.parser.parse_query(query)
