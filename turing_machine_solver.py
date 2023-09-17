import itertools
import math
from typing import Callable, List, Tuple, Iterable, Optional, Container, Sequence
import argparse

from constants import NUMBERS, QUESTIONS_PER_ROUND, VALIDATORS


class Validator:
    def __init__(self, criterions: Iterable[Callable[[int, int, int], bool]]):
        self.criterions = list(criterions)
        self.results = {}
        for i in range(len(self.criterions)):
            self.results[i] = { True: 0, False: 0 }
            for code in itertools.product(NUMBERS, NUMBERS, NUMBERS):
                r = criterions[i](*code)
                self.results[i][r] += 1
        

class Game:
    def __init__(self, validator_ids: Iterable[int]) -> None:
        self.validators = [Validator(VALIDATORS[validator_id]) for validator_id in validator_ids]

    def validate(self, v: int, code: Tuple[int, int, int], answers: Iterable[int]) -> bool:
        return self.validators[v].criterions[answers[v]](*code)


class Solver:
    def __init__(self, validator_ids: Iterable[int], *, filter_unique_answer = True, filter_useless_validators = True) -> None:
        validator_ids = list(validator_ids)
        self.game = Game(validator_ids)
        self.filter_unique_answer = filter_unique_answer
        self.filter_useless_validators = filter_useless_validators
        self.history = []
        
        print('Initializing solver for game:', validator_ids)
        for v in range(len(self.game.validators)):
            print(chr(v + ord('A')), self.game.validators[v].results)

        # find all possible hiddens, and their codes
        # a hidden is a tuple of criterion indices
        # a possible hidden is a hidden that can uniquely determine an code, i.e. only one code can satisfy all validator criterions
        self.hidden_and_codes = []
        for hidden in itertools.product(*[range(len(validator.criterions)) for validator in self.game.validators]):
            code = Solver.check_hidden_possible(hidden, self.game.validators, self.filter_unique_answer)
            if code is not None:
                self.hidden_and_codes.append((hidden, code))

        print('Possible hiddens and corresponding codes:')
        for hidden, code in self.hidden_and_codes:
            print(' -', hidden, '=>', code)
        print(f'({len(self.hidden_and_codes)} possible hiddens in total)')
                
        # filter useless validators
        # a validator is useless if code can be uniquely determined by other validators
        if self.filter_useless_validators:
            print('Filtering hiddens by checking useless validators:')
            self.hidden_and_codes = list(itertools.filterfalse(lambda h_o: self.has_useless_validators(h_o[0], h_o[1]), self.hidden_and_codes))
        else:
            print('Skip filtering hiddens by checking useless validators')

        print('Filtered hiddens and corresponding codes:')
        for hidden, code in self.hidden_and_codes:
            print(' -', hidden, '=>', code)
        print(f'({len(self.hidden_and_codes)} possible hiddens in total)')
    
    def solved(self) -> bool:
        return len(self.hidden_and_codes) == 1

    def print_solved(self):
        hidden, code = self.hidden_and_codes[0]
        print('Solved:')
        print(' - hidden:', hidden)
        print(' - code  :', code)

        rounds = []
        for query_code, query_v, query_r in self.history:
            if len(rounds) > 0 and rounds[-1][0] == query_code and len(rounds[-1][1]) < 3:
                rounds[-1][1].append((query_v, query_r))
            else:
                rounds.append((query_code, [(query_v, query_r)]))
        
        if not self.history:
            print('Solved without asking questions')
            return
        
        print('History:')
        print('       ', *[chr(v + ord('A')) for v in range(len(self.game.validators))])
        for round in rounds:
            code, round_history = round
            line = []
            for v in range(len(self.game.validators)):
                if (v, True) in round_history:
                    line.append('V')
                elif (v, False) in round_history:
                    line.append('X')
                else:
                    line.append(' ')
            print(*code, '|', *line)
    
    def next_query(self) -> List[Tuple[Tuple[int, int, int], int]]:
        '''
        returns best query: codes and validator_ids
        '''
        if len(self.hidden_and_codes) == 0:
            print('Error: Game not valid because no possible hiddens')
            return []
        if self.solved():
            self.print_solved()
            return []

        print('Find all possible queries:')
        all_queries = self.recursively_find_queries([], self.hidden_and_codes, 0.0, 1.0)
        if len(all_queries) == 0:
            print('Error: no valid query found')
        
        all_queries.sort(key=lambda x: x[1], reverse=True)
        # print top 10 queries
        for queries, entropy in all_queries[:10]:
            print(' -', self.find_code_for_query(queries), *[chr(vv + ord('A')) for _, vv in queries], f'=> {entropy:.6f}')
        if len(all_queries) > 10:
            print(f' - ... ({len(all_queries)} in total)')
        queries, entropy = all_queries[0]

        code = self.find_code_for_query(queries)
        if code is not None:
            print('[Query]', code, *[chr(v + ord('A')) for _, v in queries], f'which has entropy {entropy:.6f}')
            return [(code, v) for _, v in queries]
        return []

    def update_question_result(self, query_code: Tuple[int, int, int], query_v: int, query_r: bool):
        print('Updating question:', chr(query_v + ord('A')), query_code, '=>', r)
        self.history.append((query_code, query_v, query_r))
        self.hidden_and_codes = [(h, op) for h, op in self.hidden_and_codes if self.game.validators[query_v].criterions[h[query_v]](*query_code) == query_r]
        for hidden, code in self.hidden_and_codes:
            print(' -', hidden, '=>', code)
        print(f'({len(self.hidden_and_codes)} possible hiddens left)')
        
    def check_should_query(self, code: Tuple[int, int, int], v: int):
        rs = tuple([criterion(*code) for criterion in self.game.validators[v].criterions])
        results = { True: 0, False: 0 }
        for hidden, _ in self.hidden_and_codes:
            results[rs[hidden[v]]] += 1
        return results[True] != 0 and results[False] != 0

    @staticmethod
    def try_validate(validators: Container[Validator], hidden: Container[int], code: Tuple[int, int, int]) -> bool:
        assert(len(hidden) == len(validators))
        return all([validator.criterions[i](*code) for validator, i in zip(validators, hidden)])
    
    @staticmethod 
    def check_hidden_possible(hidden: Container[int], validators: Container[Validator], filter_unique_answer) -> Optional[Tuple[int, int, int]]:
        assert(len(hidden) == len(validators))
        codes = []
        for code in itertools.product(NUMBERS, NUMBERS, NUMBERS):
            if Solver.try_validate(validators, hidden, code):
                codes.append(code)
        if filter_unique_answer and len(codes) > 1:
            return None
        elif len(codes) > 0:
            return codes[0]
        else:
            return None

    def has_useless_validators(self, hidden: Sequence[int], code: Tuple[int, int, int]) -> bool:
        if len(hidden) == 1:
            return False
        for v in range(len(hidden)):
            other_hiddens = [hidden[x] for x in range(len(hidden)) if x != v]
            other_validators = [self.game.validators[x] for x in range(len(hidden)) if x != v]
            if Solver.check_hidden_possible(other_hiddens, other_validators, self.filter_unique_answer) is not None:
                print(' -', hidden, '=>', code, '[x] validator', chr(v + ord('A')), 'is useless')
                return True
        return False

    def recursively_find_queries(self, previous_query: List[Tuple[Sequence[bool], int]], previous_hidden_and_codes: List[Tuple[Sequence[int], Tuple[int, int, int]]], previous_entropy: float, probability: float) -> List[Tuple[List[Tuple[Sequence[bool], int]], float]]:
        if len(previous_query) == QUESTIONS_PER_ROUND:
            return []

        result_queries_and_entropies: List[Tuple[List[Tuple[List[bool], int]], float]] = []
        # choose from each validator
        for v in range(len(self.game.validators)):
            # if this validator has been queried before, skip
            if any([question[1] == v for question in previous_query]):
                continue
            codes = {}
            for code in itertools.product(NUMBERS, NUMBERS, NUMBERS):
                # check this satisfies all previous queries
                if not all([tuple([criterion(*code) for criterion in self.game.validators[question_v].criterions]) == question_rs for question_rs, question_v in previous_query]):
                    continue
                rs = tuple([criterion(*code) for criterion in self.game.validators[v].criterions])
                codes.setdefault(rs, code)

            for rs, code in codes.items():
                results = { True: 0, False: 0 }
                for hidden, _ in previous_hidden_and_codes:
                    results[rs[hidden[v]]] += 1
                if results[True] == 0 or results[False] == 0:
                    continue
                p = results[True] / (results[True] + results[False])
                entropy = -p * math.log2(p) - (1 - p) * math.log2(1 - p) if p > 0.0 and p < 1.0 else 0.0
                entropy = previous_entropy + probability * entropy

                # append to result
                query = previous_query + [(rs, v)]
                result_queries_and_entropies.append((query, entropy))

                # recursively find more queries
                hidden_and_codes_if_true = [(h, op) for h, op in previous_hidden_and_codes if self.game.validators[v].criterions[h[v]](*code) == True]
                result_queries_and_entropies.extend(self.recursively_find_queries(query, hidden_and_codes_if_true, entropy, p))
                hidden_and_codes_if_false = [(h, op) for h, op in previous_hidden_and_codes if self.game.validators[v].criterions[h[v]](*code) == False]
                result_queries_and_entropies.extend(self.recursively_find_queries(query, hidden_and_codes_if_false, entropy, 1 - p))
        return result_queries_and_entropies

    def find_code_for_query(self, query: Iterable[Tuple[Sequence[bool], int]]) -> Optional[Tuple[int, int, int]]:
        def check_code_for_question(code: Tuple[int, int, int], question: Tuple[Tuple[int, int, int], int]) -> bool:
            question_rs, question_v = question
            return tuple([criterion(*code) for criterion in self.game.validators[question_v].criterions]) == question_rs
        for code in itertools.product(NUMBERS, NUMBERS, NUMBERS):
            if all([check_code_for_question(code, question) for question in query]):
                return code
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
        solver.print_solved()
    while not solver.solved():
        query = solver.next_query()
        if not query:
            break
        for question in query:
            code, v = question
            if not solver.check_should_query(code, v):
                print('Skip question: ', chr(v + ord("A")), code)
                continue

            r = None
            while r not in ['0', '1']:
                r = input(f'> {code} {chr(v + ord("A"))}: ')
            r = bool(int(r))
            solver.update_question_result(code, v, r)
            if solver.solved():
                solver.print_solved()
                break
