class Parser:
    def __init__(self, grammar, sequence_file):
        # Initialize parser with grammar, input sequence, working set, input buffer, state, and index.
        self.grammar = grammar
        self.sequence = self.read_sequence(sequence_file)
        self.working = []
        self.input = [self.grammar.get_start_symbol()]
        self.state = "q"
        self.index = 0

    @staticmethod
    def read_sequence(seq_file):
        # Static method to read the input sequence from a file.
        seq = []
        with open(seq_file) as f:
            line = f.readline()
            while line:
                seq.append(line.strip())
                line = f.readline()
        return seq

    def get_situation(self):
        # Print the current parsing situation.
        print(f"({self.state}, {self.index}, {self.working}, {self.input})")

    def expand(self):
        # Expand the current non-terminal in the working set.
        print("|--- expand")
        non_terminal = self.input.pop(0)
        self.working.append((non_terminal, 0))
        new_production = self.grammar.get_productions_for_non_terminal(non_terminal)[0]
        self.input = new_production + self.input

    def advance(self):
        # Advance in the parsing process.
        print("|--- advance")
        self.working.append(self.input.pop(0))
        self.index += 1

    def momentary_insuccess(self):
        # Signal a momentary failure in parsing, transitioning to a backtracking state.
        print("|--- momentary insuccess")
        self.state = "b"

    def back(self):
        # Backtrack in the parsing process.
        print("|--- back")
        item = self.working.pop()
        self.input.insert(0, item)
        self.index -= 1

    def success(self):
        # Signal successful completion of parsing.
        print("|--- success")
        self.state = "f"
        msg = f"(f, {self.index}, {self.working}, {self.input})\n=> sequence is syntactically correct\n"
        print(msg)

    def another_try(self):
        # Attempt another production during backtracking.
        print("|--- another try")
        if self.working:
            last_nt = self.working.pop()
            nt, production_nr = last_nt

            productions = self.grammar.get_productions_for_non_terminal(nt)

            if production_nr + 1 < len(productions):
                self.state = "q"

                new_tuple = (nt, production_nr + 1)
                self.working.append(new_tuple)

                len_last_production = len(productions[production_nr])
                self.input = self.input[len_last_production:]
                new_production = productions[production_nr + 1]
                self.input = new_production + self.input
            else:
                len_last_production = len(productions[production_nr])
                self.input = self.input[len_last_production:]
                if not len(self.input) == 0:
                    self.input = [nt] + self.input
        else:
            self.state = "e"

    def error(self):
        # Signal an error state when no more input is available during parsing.
        print("|--- error")
        self.state = "e"
        msg = f"(e, {self.index}, {self.working}, {self.input})\nNo more input to look at!"
        print(msg)

    def run(self):
        # Execute the parsing process until a success or error state is reached.
        while (self.state != "f") and (self.state != "e"):
            self.get_situation()
            if self.state == "q":
                if len(self.input) == 0 and self.index == len(self.sequence):
                    self.success()
                else:
                    if self.input[0] in self.grammar.get_non_terminals()[0].split(" "):
                        self.expand()
                    else:
                        if self.index < len(self.sequence) and self.input[0] == self.sequence[self.index]:
                            self.advance()
                        else:
                            self.momentary_insuccess()
            else:
                if self.state == "b":
                    if self.working and self.working[-1] in self.grammar.get_terminals()[0].split(" "):
                        self.back()
                    else:
                        self.another_try()

        if self.state == "e":
            self.get_situation()
            self.error()
