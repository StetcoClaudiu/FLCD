class Parser:
    def __init__(self, cfg_grammar, sequence_file):
        self.cfg_grammar = cfg_grammar
        self.sequence = self.load_sequence(sequence_file)
        self.working_stack = []
        self.input_buffer = [self.cfg_grammar.get_start_symbol()]
        self.state = "q"
        self.index = 0

    @staticmethod
    def load_sequence(seq_file):
        seq = []
        with open(seq_file) as f:
            for line in f:
                seq.append(line.strip())
        return seq

    def current_situation(self):
        print(f"({self.state}, {self.index}, {self.working_stack}, {self.input_buffer})")

    def expand_non_terminal(self):
        non_terminal = self.input_buffer.pop(0)
        self.working_stack.append((non_terminal, 0))
        new_production = self.cfg_grammar.get_productions_for_non_terminal(non_terminal)[0]
        self.input_buffer = new_production + self.input_buffer

    def advance_parsing(self):
        self.working_stack.append(self.input_buffer.pop(0))
        self.index += 1

    def momentary_insuccess(self):
        self.state = "b"

    def backtrack(self):
        item = self.working_stack.pop()
        self.input_buffer.insert(0, item)
        self.index -= 1

    def successful_parsing(self):
        self.state = "f"
        msg = f"(f, {self.index}, {self.working_stack}, {self.input_buffer})\n=> sequence is syntactically correct\n"
        print(msg)

    def try_another_production(self):
        if self.working_stack:
            last_nt = self.working_stack.pop()
            nt, production_nr = last_nt

            productions = self.cfg_grammar.get_productions_for_non_terminal(nt)

            if production_nr + 1 < len(productions):
                self.state = "q"

                new_tuple = (nt, production_nr + 1)
                self.working_stack.append(new_tuple)

                len_last_production = len(productions[production_nr])
                self.input_buffer = self.input_buffer[len_last_production:]
                new_production = productions[production_nr + 1]
                self.input_buffer = new_production + self.input_buffer
            else:
                len_last_production = len(productions[production_nr])
                self.input_buffer = self.input_buffer[len_last_production:]
                if not len(self.input_buffer) == 0:
                    self.input_buffer = [nt] + self.input_buffer
        else:
            self.state = "e"

    def error_state(self):
        self.state = "e"
        msg = f"(e, {self.index}, {self.working_stack}, {self.input_buffer})\nNo more input to look at!"
        print(msg)

    def execute(self):
        while (self.state != "f") and (self.state != "e"):
            self.current_situation()
            if self.state == "q":
                if len(self.input_buffer) == 0 and self.index == len(self.sequence):
                    self.successful_parsing()
                else:
                    if self.input_buffer[0] in self.cfg_grammar.get_non_terminals()[0].split(" "):
                        self.expand_non_terminal()
                    else:
                        if self.index < len(self.sequence) and self.input_buffer[0] == self.sequence[self.index]:
                            self.advance_parsing()
                        else:
                            self.momentary_insuccess()
            else:
                if self.state == "b":
                    if self.working_stack and self.working_stack[-1] in self.cfg_grammar.get_terminals()[0].split(" "):
                        self.backtrack()
                    else:
                        self.try_another_production()

        if self.state == "e":
            self.current_situation()
            self.error_state()
