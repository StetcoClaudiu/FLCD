from Grammar import Grammar
from Parser import Parser
from ParserOutput import ParsingOutput

def main():
    while True:
        print("Choose an option:")
        print("1. Run Parser 1")
        print("2. Run Parser 2")
        print("0. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            sequence_file = "sequence1.txt"
            grammar_file = "grammar1.txt"
        elif choice == '2':
            sequence_file = "sequence2.txt"
            grammar_file = "grammar2.txt"
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please select a valid option.")
            continue

        cfg_grammar = Grammar()
        cfg_grammar.read_from_file(grammar_file)

        parser = Parser(cfg_grammar, sequence_file)
        parser.execute()

        parsing_output = ParsingOutput(cfg_grammar, sequence_file)
        parsing_output.build_tree(parser.working_stack)
        parsing_output.write_tree(parser.state, parser.working_stack, "tree.txt")

if __name__ == "__main__":
    main()
