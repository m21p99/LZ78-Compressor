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
		print m_len
		while i < m_len:
			print i
			# case I
			if data[i] not in tree_dict.keys():
				yield (0, data[i])
				tree_dict[data[i]] = len(tree_dict) + 1
				i += 1
			# case III
			elif i == m_len - 1:
				yield (tree_dict.get(data[i]), '')
				i += 1
			else:
				for j in range(i + 1, m_len):
					# case II
					if data[i:j + 1] not in tree_dict.keys():
						yield (tree_dict.get(data[i:j]), data[j])
						tree_dict[data[i:j + 1]] = len(tree_dict) + 1
						i = j + 1
						break
					# case III
					elif j == m_len - 1:
						yield (tree_dict.get(data[i:j + 1]), '')
						i = j + 1
		print tree_dict
		return 0


		# 	if match: 
		# 		# Add 1 bit flag, followed by 12 bit for distance, and 4 bit for the length
		# 		# of the match 
		# 		(bestMatchDistance, bestMatchLength) = match

		# 		output_buffer.append(True)
		# 		output_buffer.frombytes(chr(bestMatchDistance >> 4))
		# 		output_buffer.frombytes(chr(((bestMatchDistance & 0xf) << 4) | bestMatchLength))

		# 		if verbose:
		# 			print "<1, %i, %i>" % (bestMatchDistance, bestMatchLength),

		# 		i += bestMatchLength

		# 	else:
		# 		# No useful match was found. Add 0 bit flag, followed by 8 bit for the character
		# 		output_buffer.append(False)
		# 		output_buffer.frombytes(data[i])
				
		# 		if verbose:
		# 			print "<0, %s>" % data[i],

		# 		i += 1

		# # fill the buffer with zeros if the number of bits is not a multiple of 8		
		# output_buffer.fill()

		# # write the compressed data into a binary file if a path is provided
		# if output_file_path:
		# 	try:
		# 		with open(output_file_path, 'wb') as output_file:
		# 			output_file.write(output_buffer.tobytes())
		# 			print "File was compressed successfully and saved to output path ..."
		# 			return None
		# 	except IOError:
		# 		print 'Could not write to output file path. Please check if the path is correct ...'
		# 		raise

		# # an output file path was not provided, return the compressed data
		# return output_buffer


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

		while len(data) >= 9:

			flag = data.pop(0)

			if not flag:
				byte = data[0:8].tobytes()

				output_buffer.append(byte)
				del data[0:8]
			else:
				byte1 = ord(data[0:8].tobytes())
				byte2 = ord(data[8:16].tobytes())

				del data[0:16]
				distance = (byte1 << 4) | (byte2 >> 4)
				length = (byte2 & 0xf)

				for i in range(length):
					output_buffer.append(output_buffer[-distance])
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
	lz78.compress('test_data.txt')