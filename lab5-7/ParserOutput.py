class TreeNode:
    def __init__(self, value):
        self.father = -1
        self.sibling = -1
        self.value = value
        self.production = -1

    def __str__(self):
        return f"{self.value}  {self.father}  {self.sibling}"

class ParsingOutput:
    def __init__(self, cfg_grammar, sequence_file):
        self.cfg_grammar = cfg_grammar
        self.sequence = self.load_sequence(sequence_file)
        self.tree_nodes = []

    @staticmethod
    def load_sequence(seq_file):
        seq = []
        with open(seq_file) as f:
            for line in f:
                seq.append(line.strip())
        return seq

    def build_tree(self, working_stack):
        father = -1
        for index in range(len(working_stack)):
            if type(working_stack[index]) == tuple:
                self.tree_nodes.append(TreeNode(working_stack[index][0]))
                self.tree_nodes[index].production = working_stack[index][1]
            else:
                self.tree_nodes.append(TreeNode(working_stack[index]))

        for index in range(len(working_stack)):
            if type(working_stack[index]) == tuple:
                self.tree_nodes[index].father = father
                father = index
                len_prod = len(self.cfg_grammar.get_productions()[working_stack[index][0]][working_stack[index][1]])
                vector_indx = []
                for i in range(1, len_prod + 1):
                    vector_indx.append(index + i)
                for i in range(len_prod):
                    if self.tree_nodes[vector_indx[i]].production != -1:
                        offset = self.calculate_depth(vector_indx[i], working_stack)
                        for j in range(i + 1, len_prod):
                            vector_indx[j] += offset
                for i in range(len_prod - 1):
                    self.tree_nodes[vector_indx[i]].sibling = vector_indx[i + 1]
            else:
                self.tree_nodes[index].father = father
                father = -1

    def calculate_depth(self, index, working_stack):
        production = self.cfg_grammar.get_productions()[working_stack[index][0]][working_stack[index][1]]
        len_prod = len(production)
        sum_depth = len_prod
        for i in range(1, len_prod + 1):
            if type(working_stack[index + i]) == tuple:
                sum_depth += self.calculate_depth(index + i, working_stack)
        return sum_depth

    def write_tree(self, state, working_stack, output_file=None):
        if state != "e":
            lines = ["Parsing tree:"]
            lines.append("{:<10} {:<15} {:<10} {:<10}".format("index", "value", "father", "sibling"))

            for index in range(len(working_stack)):
                value = self.tree_nodes[index].value if self.tree_nodes[index].value else "N/A"
                lines.append("{:<10} {:<15} {:<10} {:<10}".format(index, value,
                                                                    self.tree_nodes[index].father,
                                                                    self.tree_nodes[index].sibling))

            print("\n".join(lines))

            if output_file:
                with open(output_file, "w") as file:
                    file.write("\n".join(lines))
