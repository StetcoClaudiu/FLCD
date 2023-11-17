import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;


public class Main {
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        System.out.println("Enter file name: ");
        String fileName=scanner.nextLine();

        Scanner1 myScanner=new Scanner1(fileName);
        
    }
}