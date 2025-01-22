###############
# Assignment 
###############
In this assignment you'll only need to implement a single class named "First". The First.java file should be in the src directory, where the FirstI.java, FirstException.java, and RunFirst.java files are located.

The "First" class must implement FirstI. The behavior of each of the methods from the interface is document in the javadoc of FirstI. Your First.java file should include these javadoc comments. Additionally, your "First" class will need to have a constructor. An example of the constructor call and comments regarding the constructor arguments/behavior can be found in RunFirst.java. The "First" class must not contain a main method.

For this assignment, you are free to use any editor you would like to write First.java. For later assignments, I'm going to expect everyone is using IntelliJ Community Edition as their IDE... JAVA doesn't ever care what editor you use but IntelliJ Community Edition is the IDE I'm going to use in lecture.

You must update the README.txt before you submit your assignment. Minimally, you must update the Files section to include the files you add and a comment about what that file contains/does; for this assignment the only added file should be src/First.java.

###############
# Running the Program
###############
After implementing FirstI in a class named "First", you should be able to compile the JAVA code in the src directory. The RunFirst class contains the main method to run the program.

If you use the commandline and are in the src directory, the following two lines should compile and run the program.
javac *.java
java RunFirst

If you are using an IDE, you'll need to setup a run configuration that uses RunFirst.

RunFirst should open a GUI that will ask you to select the "data" directory for the project (the directory containing "book.txt"). After selecting the directory, the GUI will display the results of creating instances of your "First" class and calling different methods.

The RunFirst class does not test interesting edge cases when run. You should probably try writing your own class to test your "First" class (just don't include that class in the zip file you submit). Think of inputs or call sequences that might be tricky for your implementation to do the right thing with, try making those calls, and verify that your implementation behaves as expected based on the javadoc for the methods.

Unit testing is a standard software development practice to try to find bugs in classes/methods and JUnit is a pretty standard unit testing framework for JAVA (I don't expect you to know how to use JUnit, we'll talk about it later in the block). The test/FirstTests.java file contains JUnit tests for your "First" implementation. These are the same functional tests that will be used to grade the functional elements of your methods. Each method in FirstTests represents a single test case and the logic in the method are the steps to perform the test. The "assert" calls are how checks are performed between the expected and actual behaviors.


###############
# Instructor's Motivation (Why assign this particular problem)
###############
TLDR; this assignment tries to demonstrate a baseline skillset to build from during the block.

This is a first programming assignment for the block and in some ways is intended to serve as a "warmup". It is not intended to be hard but could be challenging if you haven't done much JAVA programming recently or your previous JAVA exposure didn't include some language features. It's ok if this assignment initially feels hard but be sure to allocate the time to get help and improve your JAVA fluency... The coming assignments will be much longer and more involved than this one.

This assignment is checking the following JAVA topics:
- The ability to write a JAVA class based on an interface specification
- The ability to copy/write javadoc comments in your code
- The ability to write code that opens and reads a text file
- The ability to throw exceptions
- The ability to use instance variables to track state between method calls

This assignment also checks for a few more general computer use skills:
- The ability to decompress/compress data in a zip file
- The ability to work in/with the file system
- The ability to access starter code using an editor

These are all fairly complex things to be able to do as a newer programmer but are critical foundation capabilities for reading/writing object oriented code that solves large problems or involves multiple authors.


###############
# Files
###############
README.txt              Describes the contents of the codebase
src/FirstI.java         The interface to be implemented in the assignment
src/FirstException.java A custom exception to be throw in the FirstI.java implementation
src/RunFirst.java       A program that uses the First class
test/FirstTests.java    JUnit tests suite for the First class
data/no_spoon.txt       A text that does not contain the word spoon
data/10_spoons.txt      A text file that contains spoon exactly 10 times
data/book.txt           A long text file that contains MacBeth as hosted by Project Gutenberg
