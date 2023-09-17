import itertools
import math
from typing import Callable, List, Tuple, Iterable, Optional, Container, Sequence
import argparse

from constants import NUMBERS, QUERIES_PER_ROUND, VALIDATORS


class Validator:
    def __init__(self, standards: Iterable[Callable[[int, int, int], bool]]):
        self.standards = list(standards)
        self.results = {}
        for i in range(len(self.standards)):
            self.results[i] = { True: 0, False: 0 }
            for option in itertools.product(NUMBERS, NUMBERS, NUMBERS):
                r = standards[i](*option)
                self.results[i][r] += 1
        

class Game:
    def __init__(self, validator_ids: Iterable[int]) -> None:
        self.validators = [Validator(VALIDATORS[validator_id]) for validator_id in validator_ids]

    def validate(self, v: int, option: Tuple[int, int, int], answers: Iterable[int]) -> bool:
        return self.validators[v].standards[self.answers[v]](*option)


class Solver:
    def __init__(self, validator_ids: Iterable[int], *, filter_unique_answer = True, filter_useless_validators = True) -> None:
        validator_ids = list(validator_ids)
        self.game = Game(validator_ids)
        self.filter_unique_answer = filter_unique_answer
        self.filter_useless_validators = filter_useless_validators
        
        print('Initializing solver for game:', validator_ids)
        for v in range(len(self.game.validators)):
            print(chr(v + ord('A')), self.game.validators[v].results)

        # find all possible hiddens, and their options
        # a hidden is a tuple of standard indices
        # a possible hidden is a hidden that can uniquely determine an option, i.e. only one option can satisfy all validator standards
        self.hidden_and_options = []
        for hidden in itertools.product(*[range(len(validator.standards)) for validator in self.game.validators]):
            option = Solver.check_hidden_possible(hidden, self.game.validators, self.filter_unique_answer)
            if option is not None:
                self.hidden_and_options.append((hidden, option))

        print('Possible hiddens and corresponding options:')
        for hidden, option in self.hidden_and_options:
            print(' -', hidden, '=>', option)
        print(f'({len(self.hidden_and_options)} possible hiddens in total)')
                
        # filter useless validators
        # a validator is useless if option can be uniquely determined by other validators
        if self.filter_useless_validators:
            print('Filtering hiddens by checking useless validators:')
            self.hidden_and_options = list(itertools.filterfalse(lambda h_o: self.has_useless_validators(h_o[0], h_o[1]), self.hidden_and_options))
        else:
            print('Skip filtering hiddens by checking useless validators')

        print('Filtered hiddens and corresponding options:')
        for hidden, option in self.hidden_and_options:
            print(' -', hidden, '=>', option)
        print(f'({len(self.hidden_and_options)} possible hiddens in total)')
    
    def solved(self) -> bool:
        return len(self.hidden_and_options) == 1
    
    def next_query(self) -> List[Tuple[Tuple[int, int, int], int]]:
        '''
        returns best query: options and validator_id
        '''
        if len(self.hidden_and_options) == 0:
            print('Error: Game not valid because no possible hiddens')
            return []
        if self.solved():
            hidden, option = self.hidden_and_options[0]
            print('Solved:')
            print(' - hidden:', hidden)
            print(' - option:', option)
            return []

        print('Find all possible queries:')
        all_queries = self.recursively_find_queries([], self.hidden_and_options, 0.0, 1.0)
        if len(all_queries) == 0:
            print('Error: no valid query found')
        
        all_queries.sort(key=lambda x: x[1], reverse=True)
        # print top 10 queries
        for queries, entropy in all_queries[:10]:
            print(' -', self.find_option_for_queries(queries), *[chr(vv + ord('A')) for _, vv in queries], '=>', entropy)
        if len(all_queries) > 10:
            print(f' - ... ({len(all_queries)} in total)')
        queries, entropy = all_queries[0]

        option = self.find_option_for_queries(queries)
        if option is not None:
            print('[Query]', option, *[chr(v + ord('A')) for _, v in queries], 'which has entropy', entropy)
            return [(option, v) for _, v in queries]
        return []

    def update_query_result(self, query_option: Tuple[int, int, int], query_v: int, query_r: bool):
        print('Updating query:', chr(query_v + ord('A')), query_option, '=>', r)
        self.hidden_and_options = [(h, op) for h, op in self.hidden_and_options if self.game.validators[query_v].standards[h[query_v]](*query_option) == query_r]
        for hidden, option in self.hidden_and_options:
            print(' -', hidden, '=>', option)
        print(f'({len(self.hidden_and_options)} possible hiddens left)')
        
    def check_should_query(self, option: Tuple[int, int, int], v: int):
        rs = tuple([standard(*option) for standard in self.game.validators[v].standards])
        results = { True: 0, False: 0 }
        for hidden, _ in self.hidden_and_options:
            results[rs[hidden[v]]] += 1
        return results[True] != 0 and results[False] != 0

    @staticmethod
    def try_validate(validators: Container[Validator], hidden: Container[int], option: Tuple[int, int, int]) -> bool:
        assert(len(hidden) == len(validators))
        return all([validator.standards[i](*option) for validator, i in zip(validators, hidden)])
    
    @staticmethod 
    def check_hidden_possible(hidden: Container[int], validators: Container[Validator], filter_unique_answer) -> Optional[Tuple[int, int, int]]:
        assert(len(hidden) == len(validators))
        options = []
        for option in itertools.product(NUMBERS, NUMBERS, NUMBERS):
            if Solver.try_validate(validators, hidden, option):
                options.append(option)
        if filter_unique_answer and len(options) > 1:
            return None
        elif len(options) > 0:
            return options[0]
        else:
            return None

    def has_useless_validators(self, hidden: Sequence[int], option: Tuple[int, int, int]) -> bool:
        if len(hidden) == 1:
            return False
        for v in range(len(hidden)):
            other_hiddens = [hidden[x] for x in range(len(hidden)) if x != v]
            other_validators = [self.game.validators[x] for x in range(len(hidden)) if x != v]
            if Solver.check_hidden_possible(other_hiddens, other_validators, self.filter_unique_answer) is not None:
                print(' -', hidden, '=>', option, '[x] validator', chr(v + ord('A')), 'is useless')
                return True
        return False

    def recursively_find_queries(self, previous_queries: List[Tuple[Sequence[bool], int]], previous_hidden_and_options: List[Tuple[Sequence[int], Tuple[int, int, int]]], previous_entropy: float, probability: float) -> List[Tuple[List[Tuple[Sequence[bool], int]], float]]:
        if len(previous_queries) == QUERIES_PER_ROUND:
            return []

        result_queries_and_entropies: List[Tuple[List[Tuple[List[bool], int]], float]] = []
        # choose from each validator
        for v in range(len(self.game.validators)):
            # if this validator has been queried before, skip
            if any([query[1] == v for query in previous_queries]):
                continue
            options = {}
            for option in itertools.product(NUMBERS, NUMBERS, NUMBERS):
                # check this satisfies all previous queries
                if not all([tuple([standard(*option) for standard in self.game.validators[prev_v].standards]) == prev_rs for prev_rs, prev_v in previous_queries]):
                    continue
                rs = tuple([standard(*option) for standard in self.game.validators[v].standards])
                options.setdefault(rs, option)

            for rs, option in options.items():
                results = { True: 0, False: 0 }
                for hidden, _ in previous_hidden_and_options:
                    results[rs[hidden[v]]] += 1
                if results[True] == 0 or results[False] == 0:
                    continue
                p = results[True] / (results[True] + results[False])
                entropy = -p * math.log2(p) - (1 - p) * math.log2(1 - p) if p > 0.0 and p < 1.0 else 0.0
                entropy = previous_entropy + probability * entropy

                # append to result
                queries = previous_queries + [(rs, v)]
                result_queries_and_entropies.append((queries, entropy))

                # recursively find more queries
                hidden_and_options_if_true = [(h, op) for h, op in previous_hidden_and_options if self.game.validators[v].standards[h[v]](*option) == True]
                result_queries_and_entropies.extend(self.recursively_find_queries(queries, hidden_and_options_if_true, entropy, p))
                hidden_and_options_if_false = [(h, op) for h, op in previous_hidden_and_options if self.game.validators[v].standards[h[v]](*option) == False]
                result_queries_and_entropies.extend(self.recursively_find_queries(queries, hidden_and_options_if_false, entropy, 1 - p))
        return result_queries_and_entropies

    def find_option_for_queries(self, queries: Iterable[Tuple[Sequence[bool], int]]) -> Optional[Tuple[int, int, int]]:
        def check_option_for_query(option: Tuple[int, int, int], query: Tuple[Tuple[int, int, int], int]) -> bool:
            query_rs, query_v = query
            return tuple([standard(*option) for standard in self.game.validators[query_v].standards]) == query_rs
        for option in itertools.product(NUMBERS, NUMBERS, NUMBERS):
            if all([check_option_for_query(option, query) for query in queries]):
                return option
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('validator_ids', nargs='+', type=int)
    parser.add_argument('--no-filter-unique', action='store_true')
    parser.add_argument('--no-filter-useless', action='store_true')
    args = parser.parse_args()

    kwargs = {}
    if args.no_filter_unique:
        kwargs['filter_unique_answer'] = False
    if args.no_filter_useless:
        kwargs['filter_useless_validators'] = False
    
    solver = Solver(args.validator_ids, **kwargs)
    if solver.solved():
        solver.next_query()
    while not solver.solved():
        queries = solver.next_query()
        if not queries:
            break
        for query in queries:
            option, v = query
            if not solver.check_should_query(option, v):
                print('Skip query: ', chr(v + ord("A")), option)
                continue

            r = None
            while r not in ['0', '1']:
                r = input(f'> {option} {chr(v + ord("A"))}: ')
            r = bool(int(r))
            solver.update_query_result(option, v, r)
            if solver.solved():
                solver.next_query()
                break
