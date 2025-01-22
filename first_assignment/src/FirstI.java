import java.io.IOException;

/** The interface for the first programming assignment of the block
 * <P>The major work to be done for this assignment is to correctly implement the FirstI interface
 * in a class named First.</P>
 */
public interface FirstI {
    /** fills an array with integer values
     * <P>Calling this method will overwrite the integers in the values array.</P>
     * @param start the value to store at index 0
     * @param ascend true if the numbers should be in increasing order. false if the numbers should be in descending order.
     * @param values the array to fill
     */
    public void fillArray(int start, boolean ascend, int[] values);

    /** sets the filename to be used by this instance
     *  <P>This method may be called multiple times, changing the file this instance uses. Note that the filename
     *  may be set to null.</P>
     * @param filename name/path of the file this instance will read  (this may be the value null)
     */
    public void setFilename(String filename);

    /** gets the filename to be used by this instance
     * <p>If the filename has not been set yet, using the constructor or setFilename method, null should be returned.
     * In all other cases, whatever value has been given for the filename should be returned.</p>
     * @return name/path of the file this instance will read from or null
     */
    public String getFilename();

    /**
     * Counts the number of times a specific character occurs in the file used by this instance
     * <p>This method is responsible for opening the filename currently set for this instance, counting
     * the number of times the character occurs in the file, closing the file, and returning the count.</p>
     *
     * @param l the letter to search the file for
     * @return the number of times the character occurs in the file
     * @throws FirstException if the filename has not been set yet for this instance
     * @throws IOException if any kind of IOException occurs
     */
    public int seekLetter(char l) throws FirstException, IOException;
}
