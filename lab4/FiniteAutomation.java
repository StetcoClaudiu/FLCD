import java.util.*;
import java.io.BufferedReader; 
import java.io.FileReader;
public class FiniteAutomation{

    private String initialState;
    private List<String> finalStates;
    private List<String> States;
    private List<String> alphabet;
    private Map<Pair3, String> transitions;

    public FiniteAutomation(String filePath){
        initialState=new String();
        finalStates=new ArrayList<>();
        States=new ArrayList<>();
        alphabet=new ArrayList<>();
        transitions=new HashMap<>();
        try(BufferedReader br = new BufferedReader(new FileReader(filePath))){
            String line;
            line=br.readLine();
            States=Arrays.asList(line.split(" "));
            line=br.readLine();
            alphabet=Arrays.asList(line.split(" "));
            initialState=br.readLine();
            line=br.readLine();
            finalStates=Arrays.asList(line.split(" "));

            while((line = br.readLine())!=null){
                ArrayList<String> elements=new ArrayList<>(Arrays.asList(line.split(" ")));
                Pair3 states=new Pair3(elements.get(0),elements.get(1));
                String path;
                path=elements.get(2);
                transitions.put(states,path);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public Pair3 findPairForString(String searchString) {
        for (Map.Entry<Pair3, String> entry : transitions.entrySet()) {
            if (entry.getValue().equals(searchString)) {
                return entry.getKey();
            }
        }
        return null;
    }

    public boolean check(String line){
        String origin="";
        Pair3 pair;
        if(alphabet.contains(line.substring(0,1))){
             pair=findPairForString(line.substring(0,1));
             if(pair.getFirst().equals(initialState)){
                origin=pair.getSecond();
             }
             else{
                System.out.println("aici");
                return false;
             }
        }
        for(int i=1;i<line.length();i++){
            if(alphabet.contains(line.substring(i, i + 1))){
                pair=findPairForString(line.substring(i, i + 1));
                if(origin.equals(pair.getFirst())){
                    origin=pair.getSecond();
                }
                else{
                    return false;
                }
            }
            else{
                return false;

            }
        }
        if(finalStates.contains(origin))
            return true;
        return false;
    }

    public void WriteElements(){
        System.out.println("Initial state: "+initialState);
        System.out.println("Final states: " + String.join(", ", finalStates));
        System.out.println("States: " + String.join(", ", States));
        System.out.println("Alphabet: " + String.join(", ", alphabet));
        System.out.println("Transitions:");
        for (Map.Entry<Pair3, String> entry : transitions.entrySet()) {
            Pair3 key = entry.getKey();
            String value = entry.getValue();
            System.out.println(key + " -> " + value);
        }
    }
}
