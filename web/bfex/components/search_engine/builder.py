from elasticsearch_dsl.search import Search, Q
from bfex.components.search_engine.stack import Stack

bool_values = ['AND', 'OR']

class QueryBuilder(object):

    def build(self, pf_query):
        # Single term query
        query = None
        stack = Stack()

        if len(pf_query) == 1:
            pass

        for token in pf_query:
            if token in bool_values:
                q1 = stack.pop()
                q2 = stack.pop()

                result = q1 & q2 if token == 'AND' else q1 | q2
                print(result)
                stack.push(result)
            else:
                q = None
                if token[0] == 'KEYWORD':
                    q = Q('term', rake_keywords=token[1])
                else:
                    q = Q('term', rake_keywords=" ".join(token[1]))
                print(q)
                stack.push(q)

        return stack.pop()

if __name__ == "__main__":
    q = [('KEYWORD', 'algae'), ('KEYWORD', 'photosensitivity'), ('PHRASE', ['big', 'bad']), ('KEYWORD', 'bad'), 'AND', 'OR']
    builder = QueryBuilder()

    builder.build(q)