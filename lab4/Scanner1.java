import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;

public class Scanner1{
    private final ArrayList<String> operators=new ArrayList<>(Arrays.asList("+","-","*","/","~","<=","<",">",">=","!=","="));
    private final ArrayList<String> separators=new ArrayList<>(Arrays.asList("(",")","[","]","{","}",":",";",",","."));
    private final ArrayList<String> reservedWords=new ArrayList<>(Arrays.asList("space","read","write","if","else","for","while","beint","bestring","return","stop","sum"));
    private final ArrayList<String> letters=new ArrayList<>(Arrays.asList("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v",
    "w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"));
    private final ArrayList<String> numbers=new ArrayList<>(Arrays.asList("0","1","2","3","4","5","6","7","8","9"));

    private String filePath;
    private SymbolTable symbolTable;
    private SymbolTable symbolTable1;
    private ArrayList<Pair2> PIF;

    public Scanner1(String filePath){
        this.filePath=filePath;
        this.symbolTable=new SymbolTable(10);
        this.symbolTable1=new SymbolTable(10);
        this.PIF = new ArrayList<>();
        }

    public boolean hasCommonCharacters(String input) {
        for (char c : input.toCharArray()) {
            if (letters.contains(String.valueOf(c))) {
                return true;
            }
        }
        return false;
    }


    public void scan() {
        File myFile = new File(this.filePath);
        try {
            Scanner myReader = new Scanner(myFile);
            String allCode1 = "";
            while (myReader.hasNextLine()) {
                String data = myReader.nextLine();
                allCode1 = allCode1 + data;
            }
            String[] wordsArray = allCode1.split("\\s+");
            for (String wordd : wordsArray) {
                if (reservedWords.contains(wordd))
                    PIF.add(new Pair2(wordd, new Pair1(0, 0)));
                else {
                    for (int i = 0; i < wordd.length(); i++) {
                        char current = wordd.charAt(i);
                        if (operators.contains(String.valueOf(current)) || separators.contains(String.valueOf(current))) {
                            PIF.add(new Pair2(String.valueOf(current), new Pair1(0, 0)));
                        } else {
                            if (letters.contains(String.valueOf(current))||numbers.contains(String.valueOf(current))) {
                                String word = "" + current;
                                i++;
                                while (i < wordd.length() && (letters.contains(String.valueOf(wordd.charAt(i))) || numbers.contains(String.valueOf(wordd.charAt(i))))) {
                                    word = word + wordd.charAt(i);
                                    i++;
                                }
                                i--;
                                if (reservedWords.contains(word)) {
                                    PIF.add(new Pair2(word, new Pair1(0, 0)));
                                } else {
                                    if(hasCommonCharacters(word)){
                                        if(numbers.contains(String.valueOf(word.charAt(0)))){
                                            System.out.println("Syntax error");
                                            System.exit(0);
                                        }
                                        if(symbolTable.containsTerm(word)){
                                            PIF.add(new Pair2(String.valueOf(word), symbolTable.findPositionOfTerm(word)));
                                        }
                                        else{
                                            symbolTable.add(word);
                                            PIF.add(new Pair2(String.valueOf(word), symbolTable.findPositionOfTerm(word)));
                                        }
                                    }
                                    else{
                                        if(symbolTable1.containsTerm(word)){
                                            PIF.add(new Pair2(String.valueOf(word), symbolTable1.findPositionOfTerm(word)));
                                            System.out.println(word);
                                        }
                                        else{
                                            symbolTable1.add(word);
                                            PIF.add(new Pair2(String.valueOf(word), symbolTable1.findPositionOfTerm(word)));
                                            System.out.println(word);
                                        }
                                    }
                                }
                            } else {
                                System.out.println(current);
                                System.out.println("Lexical error");
                                System.exit(0);
                            }
                        }
                    }
                }
            }
            System.out.println("Lexically correct");

            
            try{
                FileWriter myWrite=new FileWriter("ST.out.txt");
                myWrite.write(symbolTable.getHashTable().toString());
                myWrite.close();

            }
            catch(IOException e){
                System.out.println(e);
            }
            try{
                FileWriter myWrite=new FileWriter("ST1.out.txt");
                myWrite.write(symbolTable1.getHashTable().toString());
                myWrite.close();

            }
            catch(IOException e){
                System.out.println(e);
            }
            try {
                FileWriter myWrite = new FileWriter("PIF.out.txt");
                for (Pair2 pair : this.PIF) {
                    myWrite.write(pair.toString() + "\n");
                }
                myWrite.close();
            }
            catch(IOException e){
                System.out.println(e);
            }

        } catch (FileNotFoundException e) {
            System.out.println("File not found: " + filePath);
        }
    }
}


