# -*- coding:utf8 -*-
import math
from bitarray import bitarray

class LZ78Compressor:
    """
    A simplified implementation of the LZ78 Compression Algorithm
    """

    def compress(self, input_file_path, output_file_path=None, verbose=False):
        """
        Given the path of an input file, its content is compressed by applying a simple 
        LZ78 compression algorithm. 
        
        If a path to the output file is provided, the compressed data is written into 
        a binary file. Otherwise, it is returned as a bitarray
        if verbose is enabled, the compression description is printed to standard output
        """
        data = None
        i = 0
        tree_dict = {}
        output_buffer = bitarray(endian='big')
        
        # read the input file 
        try:
            with open(input_file_path, 'rb') as input_file:
                data = input_file.read()
        except IOError:
            print('Could not open input file ...')
            raise
        m_len = len(data)

        # compression format: 
        # 12 bit for prefixIndex, followed by 8 bit for the character
        while i < m_len:
            # data[i] has not been recorded in dict
            if data[i:i+1] not in tree_dict:
                # Write 0 for prefixIndex (0 in 12 bits)
                output_buffer.extend([0] * 12) 
                # Write the byte (8 bits)
                output_buffer.frombytes(data[i:i+1])

                # Add to the dictionary
                tree_dict[data[i:i+1]] = len(tree_dict) + 1

                if verbose:
                    print("<0, %c>" % data[i:i+1])

                i += 1
            else:
                for j in range(i + 1, m_len + 1):
                    # Check if the substring data[i:j] is in the dictionary
                    if data[i:j] not in tree_dict:
                        # Record the prefixIndex and the new character
                        prefix_index = tree_dict[data[i:j-1]]
                        output_buffer.extend([prefix_index >> 4])  # High 8 bits of the prefixIndex
                        output_buffer.extend([prefix_index & 0xF])  # Low 4 bits of the prefixIndex
                        output_buffer.frombytes(data[j-1:j])  # Add the new character

                        # Add the new substring to the dictionary
                        tree_dict[data[i:j]] = len(tree_dict) + 1

                        if verbose:
                            print("<%i, %c>" % (prefix_index, data[j-1:j]))

                        i = j  # Move to the next segment
                        break
                    elif j == m_len:
                        # If the string ends and still in dict, handle it
                        prefix_index = tree_dict[data[i:j]]
                        output_buffer.extend([prefix_index >> 4])  # High 8 bits of the prefixIndex
                        output_buffer.extend([prefix_index & 0xF])  # Low 4 bits of the prefixIndex
                        output_buffer.frombytes(b'')  # Empty character for end of string

                        if verbose:
                            print("<%i, ''>" % prefix_index)

                        i = j  # End of string, move to next
                        break

        # Fill the buffer with zeros if the number of bits is not a multiple of 8        
        output_buffer.fill()
        print('The compression rate is', (1 - output_buffer.length() / (m_len * 8.0)))

        # Write the compressed data to a binary file if a path is provided
        if output_file_path:
            try:
                with open(output_file_path, 'wb') as output_file:
                    output_file.write(output_buffer.tobytes())
                    print("File was compressed successfully and saved to output path ...")
                    return None
            except IOError:
                print('Could not write to output file path. Please check if the path is correct ...')
                raise

        # Return the compressed data as a bitarray
        return output_buffer

    def decompress(self, input_file_path, output_file_path=None):
        """
        Given the path of a compressed file, the data is decompressed back to its 
        original form, and written into the output file path if provided. 
        If no output file path is provided, the decompressed data is returned as a string.
        """
        data = bitarray(endian='big')
        output_buffer = []

        # Read the input file
        try:
            with open(input_file_path, 'rb') as input_file:
                data.fromfile(input_file)
        except IOError:
            print('Could not open input file ...')
            raise

        while len(data) >= 20:
            # Extract the 12-bit prefixIndex (split into 8 high bits and 4 low bits)
            prefixIndex = (data[0:8].tobytes()[0] << 4) | (data[8:12].tobytes()[0] >> 4)
            byte = data[12:20].tobytes()

            if prefixIndex == 0:
                # If prefixIndex is 0, just append the character
                output_buffer.append(byte)
            else:
                # Otherwise, append the previous string + new byte
                output_buffer.append(output_buffer[prefixIndex - 1] + byte)

            # Remove the first 20 bits (12 for index, 8 for the character)
            del data[0:20]

        out_data = b''.join(output_buffer)

        if output_file_path:
            try:
                with open(output_file_path, 'wb') as output_file:
                    output_file.write(out_data)
                    print('File was decompressed successfully and saved to output path ...')
                    return None
            except IOError:
                print('Could not write to output file path. Please check if the path is correct ...')
                raise

        return out_data


if __name__ == '__main__':
    lz78 = LZ78Compressor()
    lz78.compress('input.txt', 'compressed_data.lz78', False)
    lz78.decompress('compressed_data.lz78', 'decompressed_data.txt')
