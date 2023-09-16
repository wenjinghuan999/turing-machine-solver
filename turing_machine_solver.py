import itertools
import math
from typing import Callable, List, Tuple, Iterable, Optional, Container, Sequence
import argparse

from constants import NUMBERS, VALIDATORS


class Validator:
    def __init__(self, standards: Iterable[Callable[[int, int, int], bool]]):
        self.standards = list(standards)
        self.results = {}
        for i in range(len(self.standards)):
            self.results[i] = { True: 0, False: 0 }
            for t, s, c in itertools.product(NUMBERS, NUMBERS, NUMBERS):
                r = standards[i](t, s, c)
                self.results[i][r] += 1
        

class Game:
    def __init__(self, validator_ids: Iterable[int]) -> None:
        self.validators = [Validator(VALIDATORS[validator_id]) for validator_id in validator_ids]

    def validate(self, v: int, option: Tuple[int, int, int], answers: Iterable[int]) -> bool:
        return self.validators[v].standards[self.answers[v]](*option)


class Solver:
    def __init__(self, validator_ids: Iterable[int]) -> None:
        validator_ids = list(validator_ids)
        self.game = Game(validator_ids)
        
        print('Initializing solver for game:', validator_ids)
        for v in range(len(self.game.validators)):
            print(chr(v + ord('A')), self.game.validators[v].results)

        # find all possible hiddens, and their options
        # a hidden is a tuple of standard indices
        # a possible hidden is a hidden that can uniquely determine an option, i.e. only one option can satisfy all validator standards
        self.hidden_and_options = []
        for hidden in itertools.product(*[range(len(validator.standards)) for validator in self.game.validators]):
            option = Solver.check_hidden_possible(hidden, self.game.validators)
            if option is not None:
                self.hidden_and_options.append((hidden, option))

        print('Possible hiddens and corresponding options:')
        for hidden, option in self.hidden_and_options:
            print(' -', hidden, '=>', option)
                
        # filter useless validators
        # a validator is useless if option can be uniquely determined by other validators
        print('Filtering hiddens:')
        self.hidden_and_options = list(itertools.filterfalse(lambda h_o: self.has_useless_validators(h_o[0], h_o[1]), self.hidden_and_options))

        print('Filtered hiddens and corresponding options:')
        for hidden, option in self.hidden_and_options:
            print(' -', hidden, '=>', option)
    
    def next_query(self) -> Optional[Tuple[Tuple[int, int, int], int]]:
        '''
        returns best query: options and validator_id
        '''
        if len(self.hidden_and_options) == 0:
            print('Error: Game not valid because no possible hiddens')
            return None
        if len(self.hidden_and_options) == 1:
            hidden, option = self.hidden_and_options[0]
            print('Solved:')
            print(' - hidden:', hidden)
            print(' - option:', option)
            return None

        query_and_entropies = self.calc_entropy()
        if len(query_and_entropies) == 0:
            print('Error: Game not valid no query can provide infomation')
            return None
        
        option, v, entropy = query_and_entropies[0]
        print('Best query:', chr(v + ord('A')), option, 'which has entropy', entropy)
        return option, v

    def update_query_result(self, option: Tuple[int, int, int], v: int, r: bool):
        print('Updating query:', chr(v + ord('A')), option, '=>', r)
        self.hidden_and_options = [(h, op) for h, op in self.hidden_and_options if self.game.validators[v].standards[h[v]](*option) == r]

    @staticmethod
    def try_validate(validators: Container[Validator], hidden: Container[int], option: Tuple[int, int, int]) -> bool:
        assert(len(hidden) == len(validators))
        return all([validator.standards[i](*option) for validator, i in zip(validators, hidden)])
    
    @staticmethod 
    def check_hidden_possible(hidden: Container[int], validators: Container[Validator]) -> Optional[Tuple[int, int, int]]:
        assert(len(hidden) == len(validators))
        options = []
        for option in itertools.product(NUMBERS, NUMBERS, NUMBERS):
            if Solver.try_validate(validators, hidden, option):
                options.append(option)
        if len(options) == 1:
            return options[0]
        else:
            return None

    def has_useless_validators(self, hidden: Sequence[int], option: Tuple[int, int, int]) -> bool:
        if len(hidden) == 1:
            return False
        for v in range(len(hidden)):
            other_hiddens = [hidden[x] for x in range(len(hidden)) if x != v]
            other_validators = [self.game.validators[x] for x in range(len(hidden)) if x != v]
            if Solver.check_hidden_possible(other_hiddens, other_validators) is not None:
                print(' -', hidden, '=>', option, '[x] validator', chr(v + ord('A')), 'is useless')
                return True
        return False
    
    def calc_entropy(self) -> List[Tuple[Tuple[int, int, int], int, float]]:
        query_and_entropies = []
        print('Calculate entropy for each validator and each option:')
        for v in range(len(self.game.validators)):
            options = {}
            for t, s, c in itertools.product(NUMBERS, NUMBERS, NUMBERS):
                rs = tuple([standard(t, s, c) for standard in self.game.validators[v].standards])
                options.setdefault(rs, (t, s, c))

            for rs, option in options.items():
                results = { True: 0, False: 0 }
                for hidden, _ in self.hidden_and_options:
                    results[rs[hidden[v]]] += 1
                if results[True] == 0 or results[False] == 0:
                    continue
                p = results[True] / (results[True] + results[False])
                entropy = -p * math.log2(p) - (1 - p) * math.log2(1 - p) if p > 0.0 and p < 1.0 else 0.0
                query_and_entropies.append((option, v, entropy))
                print(' -', chr(v + ord('A')), rs, f'e.g.{option}', '=>', entropy)
        
        query_and_entropies.sort(key=lambda x: x[2], reverse=True)
        return query_and_entropies


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('validator_ids', nargs='+', type=int)
    args = parser.parse_args()
    
    solver = Solver(args.validator_ids)
    while True:
        query = solver.next_query()
        if query is None:
            break
        option, v = query
        r = None
        while r not in ['0', '1']:
            r = input(f'> {chr(v + ord("A"))} {option}: ')
        r = bool(int(r))
        solver.update_query_result(option, v, r)
