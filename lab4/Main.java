import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
    System.out.println("Choose between Scanner and FA\n1. Scanner\n2. FA\nChoose option: ");
    int command = scanner.nextInt();
    scanner.nextLine();  // Consume the newline character

    System.out.println("Enter file name: ");
    String fileName = scanner.nextLine();

    if (command == 1) {
        Scanner1 myScanner = new Scanner1(fileName);
        myScanner.scan();
    }
    if (command == 2) {
        FiniteAutomation myFA = new FiniteAutomation(fileName);
        int command1 = 1;
        while (command1 != 0) {
            System.out.println("\n1. Write the elements\n2. Check an DFA\n0. Exit\nChoose an option: ");
            command1 = Integer.parseInt(scanner.nextLine().trim());
            if (command1 == 1) {
                myFA.WriteElements();
            }
            if (command1 == 2) {
                System.out.println("Enter the sequence: ");
                String sequence = scanner.nextLine();
                System.out.println(myFA.check(sequence));
            }
        }
    }
    }
}