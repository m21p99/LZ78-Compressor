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
			print 'Could not open input file ...'
			raise
		m_len = len(data)
		while i < m_len:
			# data[i] has not recorded in dict, 16 bit for prefixIndex, and 8 bit for the character
			if data[i] not in tree_dict.keys():
				output_buffer.frombytes(chr(0 >> 8))
				output_buffer.frombytes(chr(0 & 0xff))
				output_buffer.frombytes(data[i])

				tree_dict[data[i]] = len(tree_dict) + 1

				if verbose:
					print "<0, %c>" % data[i]

				i += 1
			# if data[i] is the last char of string and already in dict, 16 bit for prefixIndex, and 8 bit for the character
			elif i == m_len - 1:
				output_buffer.frombytes(chr(tree_dict[data[i]] >> 8))
				output_buffer.frombytes(chr(tree_dict[data[i]] & 0xff))
				output_buffer.frombytes(data[i])

				if verbose:
					print "<%i, %c>" % (tree_dict[data[i]], data[i])

				i += 1
			else:
				for j in range(i + 1, m_len):
					# substring is not in dict
					if data[i:j + 1] not in tree_dict.keys():
						tree_dict[data[i:j + 1]] = len(tree_dict) + 1

						output_buffer.frombytes(chr(tree_dict[data[i:j]] >> 8))
						output_buffer.frombytes(chr(tree_dict[data[i:j]] & 0xff))
						output_buffer.frombytes(data[j])

						if verbose:
							print "<%i, %c>" % (tree_dict[data[i:j]], data[j])

						i = j + 1
						break
					# substring is still in dict and string has run out
					elif j == m_len - 1:
						output_buffer.frombytes(chr(tree_dict[data[i:j + 1]] >> 8))
						output_buffer.frombytes(chr(tree_dict[data[i:j + 1]] & 0xff))
						output_buffer.frombytes('')

						if verbose:
							print "<%i, ''>" % tree_dict[data[i]]
						i = j + 1

		# fill the buffer with zeros if the number of bits is not a multiple of 8		
		output_buffer.fill()

		# write the compressed data into a binary file if a path is provided
		if output_file_path:
			try:
				with open(output_file_path, 'wb') as output_file:
					output_file.write(output_buffer.tobytes())
					print "File was compressed successfully and saved to output path ..."
					return None
			except IOError:
				print 'Could not write to output file path. Please check if the path is correct ...'
				raise

		# an output file path was not provided, return the compressed data
		return output_buffer


	def decompress(self, input_file_path, output_file_path=None):
		"""
		Given a string of the compressed file path, the data is decompressed back to its 
		original form, and written into the output file path if provided. If no output 
		file path is provided, the decompressed data is returned as a string
		"""
		data = bitarray(endian='big')
		output_buffer = []

		# read the input file
		try:
			with open(input_file_path, 'rb') as input_file:
				data.fromfile(input_file)
		except IOError:
			print 'Could not open input file ...'
			raise

		while len(data) > 0:

			prefixIndex = (ord(data[0:8].tobytes()) << 8) | (ord(data[8:16].tobytes()))
			byte = data[16:24].tobytes()

			if prefixIndex == 0:
				output_buffer.append(byte)
				
			else:
				output_buffer.append(output_buffer[prefixIndex - 1] + byte)

			del data[0:24]

		out_data =  ''.join(output_buffer)

		if output_file_path:
			try:
				with open(output_file_path, 'wb') as output_file:
					output_file.write(out_data)
					print 'File was decompressed successfully and saved to output path ...'
					return None 
			except IOError:
				print 'Could not write to output file path. Please check if the path is correct ...'
				raise 
		return out_data


if __name__ == '__main__':
	lz78 = LZ78Compressor()
	lz78.compress('source_data.txt','compressed_data.lz78', False)
	lz78.decompress('compressed_data.lz78', 'decompressed_data.txt')