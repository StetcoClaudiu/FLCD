from grammar import Grammar

class LLParser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first_sets = {}
        self.follow_sets = {}
        self.parsing_table = {}
        self.construct_first_sets()
        self.construct_follow_sets()
        self.construct_parsing_table()

    def construct_first_sets(self):
        for nt in self.grammar.non_terminals:
            self.first_sets[nt] = set()
        for nt in self.grammar.non_terminals:
            self.calculate_first_set(nt)

    def calculate_first_set(self, nt):
        if nt in self.first_sets[nt]:
            return
        for prod in self.grammar.productions[(nt,)]:
            if prod[0][0] in self.grammar.terminals:
                self.first_sets[nt].add(prod[0][0])
            elif prod[0][0] in self.grammar.non_terminals:
                self.calculate_first_set(prod[0][0])
                self.first_sets[nt] |= self.first_sets[prod[0][0]]

    def construct_follow_sets(self):
        for nt in self.grammar.non_terminals:
            self.follow_sets[nt] = set()
        self.follow_sets[self.grammar.starting_nt].add('$')
        for nt in self.grammar.non_terminals:
            self.calculate_follow_set(nt)

    def calculate_follow_set(self, nt):
        for prod in self.grammar.productions.keys():
            for prod_value in self.grammar.productions[prod]:
                if nt in prod_value[0]:
                    idx = prod_value[0].index(nt)
                    if idx < len(prod_value[0]) - 1:
                        if prod_value[0][idx + 1] in self.grammar.terminals:
                            self.follow_sets[nt].add(prod_value[0][idx + 1])
                        elif prod_value[0][idx + 1] in self.grammar.non_terminals:
                            self.follow_sets[nt] |= self.first_sets[prod_value[0][idx + 1]]
                            if '' in self.first_sets[prod_value[0][idx + 1]]:
                                self.follow_sets[nt] |= self.follow_sets[prod[0][idx + 1]]

    def construct_parsing_table(self):
        for nt in self.grammar.productions.keys():
            for prod_value in self.grammar.productions[nt]:
                first_set = self.first_sets[nt[0]]  # Adjust the index if needed
                for term in first_set:
                    self.parsing_table[(nt[0], term)] = prod_value

                if '' in first_set:
                    follow_set = self.follow_sets[nt[0]]  # Adjust the index if needed
                    for term in follow_set:
                        self.parsing_table[(nt[0], term)] = prod_value

    def parse(self, input_str):
        stack = ['$']
        input_str += '$'
        input_index = 0
        stack_top = stack[-1]

        while stack_top != '$':
            if stack_top in self.grammar.terminals:
                if stack_top == input_str[input_index]:
                    stack.pop()
                    input_index += 1
                else:
                    print("Error: Mismatch between stack and input.")
                    return False
            elif stack_top in self.grammar.non_terminals:
                if (stack_top, input_str[input_index]) in self.parsing_table:
                    production = self.parsing_table[(stack_top, input_str[input_index])]
                    stack.pop()
                    if production[0] != '':
                        stack += list(production[0])[::-1]
                else:
                    print("Error: No entry in parsing table.")
                    return False
            else:
                print("Error: Invalid symbol on the stack.")
                return False

            stack_top = stack[-1]

        print("Input accepted.")
        return True


if __name__ == "__main__":
    grammar = Grammar("g1.txt")
    ll_parser = LLParser(grammar)

    input_string = input("Enter the string to parse: ")
    ll_parser.parse(input_string)
