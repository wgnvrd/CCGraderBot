import javax.swing.*;
import java.io.File;
import java.io.IOException;

/** Program to exercise First implementations */
public class RunFirst {
    /** Program's main method
     * <P>If no commandline arguments are given, the user will be prompted with a GUI to select the data directory. If
     * a single commandline argument is given, the argument will be assumed to be the path to the data directory. If
     * more than one commandline argument is given, a usage message will be displayed.</P>
     * @param args Maybe the path to the data directory
     */
    public static void main(String[] args) {
        // Check the number of commandline arguments given and figure out the data directory
        File datadir;
        if(args.length == 0) {
            // Prompt user for data directory
            JFileChooser fc = new JFileChooser(System.getProperty("user.dir"));
            fc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
            fc.showOpenDialog(null);
            datadir = fc.getSelectedFile();
            if(datadir == null) {
                System.out.println("No directory selected...");
                System.exit(1);
            }
        } else if(args.length == 1) {
            // get the data directory from the CLI args
            datadir = new File(args[0]);
        } else {
            // Incorrectly called, generate the usage message and exit
            System.out.println("Incorrect number of arguments...");
            System.out.println("Usage: java RunFirst <data dir>");
            System.exit(1);
            return;
        }

        // Checks for FirstException being thrown in different use cases
        FirstI inst;
        inst = new First(null);
        try {
            inst.seekLetter('a');
            System.out.println("seekLetter should throw an exception if the filename is unset at construction.");
        } catch(FirstException e) {
            System.out.println("Correct exception throw if the filename is unset is unset at construction.");
        } catch(IOException e) { }
        inst.setFilename("blah");
        try {
            if(inst.getFilename().equals("blah")) {
                System.out.println("Filename was set correctly using setFilename.");
            } else {
                System.out.println("Filename was incorrectly set using setFilename.");
            }
            inst.seekLetter('a');
        } catch(FirstException e) {
            System.out.println("Filename was set using setFilename method but the exception was thrown.");
        } catch(IOException e) { }
        inst = new First("huzzah");
        try {
            if(inst.getFilename().equals("huzzah")) {
                System.out.println("Filename was set correctly using constructor.");
            } else {
                System.out.println("Filename was incorrectly set using constructor.");
            }
            inst.seekLetter('a');
        } catch(FirstException e) {
            System.out.println("Filename was set using the constructor but the exception was thrown.");
        } catch(IOException e) { }

        // Check the fillArray in some different cases
        inst = new First(null);
        int[] nums = new int[5];
        inst.fillArray(-2, true, nums);
        System.out.println("Expect: -2,-1,0,1,2");
        printIntArray(nums);
        inst.fillArray( 2, false, nums);
        System.out.println("Expect: 2,1,0,-1,-2");
        printIntArray(nums);

        // Check the counts to see if they match expectations
        try {
            int c;
            inst.setFilename((new File(datadir, "no_spoon.txt")).toString());
            c = inst.seekLetter('a');
            if (c == 2) {
                System.out.println(c + " 'a's expected in no_spoon.txt and that many were found.");
            } else {
                System.out.println("2 'a's expected in no_spoon.txt and " + c + " were found.");
            }
            c = inst.seekLetter('z');
            if (c == 0) {
                System.out.println(c + " 'z's expected in no_spoon.txt and that many were found.");
            } else {
                System.out.println("0 'z's expected in no_spoon.txt and " + c + " were found.");
            }
            inst.setFilename((new File(datadir, "book.txt")).toString());
            c = inst.seekLetter('a');
            if (c == 6082) {
                System.out.println(c + " 'a's expected in book.txt and that many were found.");
            } else {
                System.out.println("6082 'a's expected in book.txt and " + c + " were found.");
            }
            c = inst.seekLetter('z');
            if (c == 30) {
                System.out.println(c + " 'z's expected in book.txt and that many were found.");
            } else {
                System.out.println("30 'z's expected in book.txt and " + c + " were found.");
            }
        } catch(Exception e) {
            System.out.println("Checking letter counts failed unexpectedly...");
        }
    }

    public static void printIntArray(int[] nums) {
        System.out.print("Actual: ");
        if(nums.length>0) {
            System.out.print(nums[0]);
        }
        for(int i=1; i<nums.length; i++) {
            System.out.print(",");
            System.out.print(nums[i]);
        }
        System.out.println("");
    }
}
