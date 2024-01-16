from LL import LLParser
from grammar import Grammar


def menu(gr, ll_parser):
    while True:
        inp = input(">")
        if inp == "1":
            print(gr.non_terminals)
        elif inp == "2":
            print(gr.terminals)
        elif inp == "3":
            print(gr.starting_nt)
        elif inp == "4":
            print(gr.productions)
        elif inp == "5":
            print(gr.cfg_check())
        elif inp == "0":
            break
        else:
            print("Invalid action!")


def print_menu():
    print("1. Print the set of non-terminals\n"
          "2. Print the set of terminals\n"
          "3. Print the starting non-terminal\n"
          "4. Print the productions\n"
          "5. Check if the grammar is context-free\n"
          "0. Exit\n\n")


if __name__ == "__main__":
    grammar = Grammar("g1.txt")
    ll_parser = LLParser(grammar)

    print_menu()
    menu(grammar, ll_parser)