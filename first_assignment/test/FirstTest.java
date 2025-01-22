import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestReporter;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

class FirstTest {
    ///////////////////////////////////////////////////////
    // fillArray tests...
    ///////////////////////////////////////////////////////
    @Test
    void fillArrayUpZero(TestReporter r) {
        int[] data = new int[10];
        FirstI f = new First(null);
        f.fillArray(0, true, data);

        assertArrayEquals(new int[]{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}, data);

        // Generate a report line
        String TEST = Thread.currentThread().getStackTrace()[1].getMethodName();
        r.publishEntry(TEST+" -> passed");
    }
    @Test
    void fillArrayDownZero(TestReporter r) {
        int[] data = new int[10];
        FirstI f = new First(null);
        f.fillArray(0, false, data);

        assertArrayEquals(new int[]{0, -1, -2, -3, -4, -5, -6, -7, -8, -9}, data);

        // Generate a report line
        String TEST = Thread.currentThread().getStackTrace()[1].getMethodName();
        r.publishEntry(TEST+" -> passed");
    }
    @Test
    void fillArrayUpNonzero(TestReporter r) {
        int[] data = new int[5];
        FirstI f = new First(null);
        f.fillArray(-2, true, data);

        assertArrayEquals(new int[]{-2, -1, 0, 1, 2}, data);

        // Generate a report line
        String TEST = Thread.currentThread().getStackTrace()[1].getMethodName();
        r.publishEntry(TEST+" -> passed");
    }
    @Test
    void fillArrayDownNonzero(TestReporter r) {
        int[] data = new int[5];
        FirstI f = new First(null);
        f.fillArray(2, false, data);

        assertArrayEquals(new int[]{2, 1, 0, -1, -2}, data);

        // Generate a report line
        String TEST = Thread.currentThread().getStackTrace()[1].getMethodName();
        r.publishEntry(TEST+" -> passed");
    }


    ///////////////////////////////////////////////////////
    // filename set/get tests...
    ///////////////////////////////////////////////////////
    @Test
    void unsetFilename(TestReporter r) {
        FirstI f = new First(null);
        assertNull(f.getFilename());

        try {
            f.seekLetter('a');
            fail("Should throw FirstException if the filename has yet to be set and seekLetter called.");
        } catch (FirstException e) {
            // Expected, pass this test
        } catch (IOException e) {
            fail("Should check if the name has been set prior to trying to access the file.");
        }

        // Generate a report line
        String TEST = Thread.currentThread().getStackTrace()[1].getMethodName();
        r.publishEntry(TEST+" -> passed");
    }
    @Test
    void existingFilenameSet(TestReporter r) {
        FirstI f = new First(null);
        assertNull(f.getFilename());
        f.setFilename("data/no_spoon.txt");
        assertEquals("data/no_spoon.txt",f.getFilename());

        try {
            f.seekLetter('a');
        } catch (FirstException e) {
            fail("FirstException thrown for the no_spoon.txt file, which should exist.");
        } catch (IOException e) {
            fail("IOException thrown for the no_spoon.txt file, which should exist.");
        }

        // Generate a report line
        String TEST = Thread.currentThread().getStackTrace()[1].getMethodName();
        r.publishEntry(TEST+" -> passed");
    }
    @Test
    void nonexistingFilename(TestReporter r) {
            FirstI f = new First(null);
            assertNull(f.getFilename());
            f.setFilename("/blah/blah.txt");
            assertEquals("/blah/blah.txt",f.getFilename());

            try {
                f.seekLetter('a');
                fail("The file to seekLetter in can't exist.");
            } catch (FirstException e) {
                fail("FirstException thrown after the file has been set.");
            } catch (IOException e) {
                // Expected
            }

            // Generate a report line
            String TEST = Thread.currentThread().getStackTrace()[1].getMethodName();
            r.publishEntry(TEST+" -> passed");
    }
    @Test
    void existingFilenameConstructor(TestReporter r) {
        FirstI f = new First("data/no_spoon.txt");
        assertEquals("data/no_spoon.txt",f.getFilename());

        try {
            f.seekLetter('a');
        } catch (FirstException e) {
            fail("FirstException thrown for the no_spoon.txt file, which should exist.");
        } catch (IOException e) {
            fail("IOException thrown for the no_spoon.txt file, which should exist.");
        }

        // Generate a report line
        String TEST = Thread.currentThread().getStackTrace()[1].getMethodName();
        r.publishEntry(TEST+" -> passed");
    }

    ///////////////////////////////////////////////////////
    // seekLetter tests...
    ///////////////////////////////////////////////////////
    @Test
    void seekLetterSetOnceConstructor(TestReporter r) throws Exception {
        FirstI f = new First("data/no_spoon.txt");
        assertEquals("data/no_spoon.txt",f.getFilename());

        assertEquals(4, f.seekLetter('o'));
        assertEquals(3, f.seekLetter('n'));

        // Generate a report line
        String TEST = Thread.currentThread().getStackTrace()[1].getMethodName();
        r.publishEntry(TEST+" -> passed");
    }
    @Test
    void seekLetterSetOnceSetMethod(TestReporter r) throws Exception {
        FirstI f = new First(null);
        assertNull(f.getFilename());
        f.setFilename("data/no_spoon.txt");
        assertEquals("data/no_spoon.txt",f.getFilename());

        assertEquals(4, f.seekLetter('o'));
        assertEquals(3, f.seekLetter('n'));

        // Generate a report line
        String TEST = Thread.currentThread().getStackTrace()[1].getMethodName();
        r.publishEntry(TEST+" -> passed");
    }
    @Test
    void seekLetterSetTwice(TestReporter r) throws Exception {
        FirstI f = new First(null);
        assertNull(f.getFilename());
        f.setFilename("data/no_spoon.txt");
        assertEquals("data/no_spoon.txt",f.getFilename());

        assertEquals(4, f.seekLetter('o'));
        assertEquals(3, f.seekLetter('n'));

        f.setFilename("data/book.txt");
        assertEquals(6678, f.seekLetter('o'));
        assertEquals(5354, f.seekLetter('n'));

        // Generate a report line
        String TEST = Thread.currentThread().getStackTrace()[1].getMethodName();
        r.publishEntry(TEST+" -> passed");
    }
}