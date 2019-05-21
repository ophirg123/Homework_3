import Huffman_code_interface
from functools import total_ordering
import os
import math


class HuffmanCoding(Huffman_code_interface.HuffmanCoding):
    """ Compress and Decompress files with calculating the entropy of the target file.

    :param path_of_file: The path of the target file to compress."""

    def __init__(self, input_file_path):
        """ Create the compressed file

        :param input_file_path: The path of the target file to compress."""


        def file_type_of_given_file_to_compress(path_of_file):
            """ Check type of file: Bin or Text

            :param path_of_file: The path of the target file to compress.
            :rtype: A: The type of the file as string."""
            if path_of_file.endswith('.bin'):
                type = "bin"
            elif path_of_file.endswith('.txt'):
                type = "txt"
            else:
                raise TypeError('This is not Text file or Bin file')
            return type

        def create_word_dictionary(word_dictionary, file_word_list):
            """ Create a dictionary of the frequency of every letter or byte in a file.

           :param word_dictionary: Dictionary with all possible symbols and frequency of each symbol.
           :rtype: B: The updated file word list as list."""

            # Read the file in relative to the extension bin.
            if self.given_file_type == "bin":
                with open(self.input_file_path, 'rb') as file:
                    file_word_string = file.read()
                for binary_number in file_word_string:
                    file_word_list.append(binary_number)

                    # Check if the symbol is in the dictionary and update the frequency
                    if binary_number in word_dictionary:
                        word_dictionary[binary_number] += 1
                    else:
                        word_dictionary[binary_number] = 1

            # Read the file in relative to the extension txt.
            else:
                with open(self.input_file_path, 'r') as file:
                    file_word_list = file.readlines()
                for word in file_word_list:
                    for l in word:

                        # Check if the symbol is in the dictionary and update the frequency
                        if l in word_dictionary:
                            word_dictionary[l] += 1
                        else:
                            word_dictionary[l] = 1
            return [word_dictionary, file_word_list]

        def tree_build_txt(elements_list):
            """ Create a node in Huffman tree for encoding each symbol for text file.

           :param elements_list: The list with the symbols and the nodes.
           :rtype: A: An instance of Node class as object"""

            # Check if the first and the second objects in list are strings
            if type(elements_list[0][0]) == str or type(elements_list[1][0]) == str:
                # Check with one of them is not and create node object from them.
                if type(elements_list[0][0]) == str:
                    tmp_1 = Node(elements_list[0][0], elements_list[0][1])
                    tmp_1.left = None
                    tmp_1.right = None
                    tmp_1.data = elements_list[0][0]
                    tmp_1.frequency = elements_list[0][1]
                    tmp_1.leaf = True
                    if type(elements_list[1][0]) != str:
                        tmp_2 = elements_list[1][0]
                if type(elements_list[1][0]) == str:
                    tmp_2 = Node(elements_list[1][0], elements_list[1][1])
                    tmp_2.left = None
                    tmp_2.right = None
                    tmp_2.data = elements_list[1][0]
                    tmp_2.frequency = elements_list[1][1]
                    tmp_2.leaf = True
                    if type(elements_list[0][0]) != str:
                        tmp_1 = elements_list[0][0]
                node = Node(tmp_1, tmp_2)
                node.data = tmp_1.data + tmp_2.data
                node.frequency = tmp_1.frequency + tmp_2.frequency
            else:
                node = Node(elements_list[0][0], elements_list[1][0])
                node.data = elements_list[0][0].data + elements_list[1][0].data
                node.frequency = elements_list[0][0].frequency + elements_list[1][0].frequency
            # Add the new Node to the element list.
            elements_list.append((node, node.frequency))
            # Remove the two elements that has been connected from the element list.
            elements_list.pop(0), elements_list.pop(0)
            return node

        def tree_build_bin(elements_list):
            """ Create a node in Huffman tree for encoding each symbol for bin file.

           :param elements_list: The list with the symbols and the nodes.
           :rtype: A: An instance of Node class as object"""

            # Check if the first and the second objects in list are Integers
            if type(elements_list[0][0]) == int or type(elements_list[1][0]) == int:
                # Check with one of them is not and create node object from them.
                if type(elements_list[0][0]) == int:
                    tmp_1 = Node(elements_list[0][0], elements_list[0][1])
                    tmp_1.left = None
                    tmp_1.right = None
                    tmp_1.data = elements_list[0][0]
                    tmp_1.frequency = elements_list[0][1]
                    tmp_1.leaf = True
                    if type(elements_list[1][0]) != int:
                        tmp_2 = elements_list[1][0]
                if type(elements_list[1][0]) == int:
                    tmp_2 = Node(elements_list[1][0], elements_list[1][1])
                    tmp_2.left = None
                    tmp_2.right = None
                    tmp_2.data = elements_list[1][0]
                    tmp_2.frequency = elements_list[1][1]
                    tmp_2.leaf = True
                    if type(elements_list[0][0]) != int:
                        tmp_1 = elements_list[0][0]
                node = Node(tmp_1, tmp_2)
                node.data = tmp_1.data + tmp_2.data
                node.frequency = tmp_1.frequency + tmp_2.frequency
            else:
                node = Node(elements_list[0][0], elements_list[1][0])
                node.data = elements_list[0][0].data + elements_list[1][0].data
                node.frequency = elements_list[0][0].frequency + elements_list[1][0].frequency
            # Add the new Node to the element list.
            elements_list.append((node, node.frequency))
            # Remove the two elements that has been connected from the element list.
            elements_list.pop(0), elements_list.pop(0)
            return node

        def create_word_binary_dictionary(trie, coding_dictionary):
            """ Create the coding dictionary with each symbol and frequency in binary number.

           :param trie: The Huffman tree.
           :param coding_dictionary: An empty dictionary to fill in.
           :rtype: A: A dictionary of with keys as strings(text file) or integers(bin file) and values as strings"""
            # Use method of Node class to search the binary value of each symbol
            trie[0][0].search_element(coding_dictionary)
            return self.coding_dictionary

        def create_compressed_file(compressed_file_path, file_word_list, coding_dictionary, file_type):
            """ Create the compressed file as bin file.

           :param compressed_file_path: The path for the compressed file.
           :param file_word_list: The list for encoding each symbol in the target file as binary number.
           :param coding_dictionary: The dictionary for encoding.
           :param file_type: The type the target file to compress."""

            # Open new file and write the binary code as bytes
            with open(compressed_file_path, 'wb') as f:
                coded_pharse = ''
                if file_type == 'bin':
                    for number in file_word_list:
                        # Change each symbol to a byte
                        coded_pharse += str(coding_dictionary.get(number))
                        if len(coded_pharse) >= 8:
                            f.write(bytearray([int(coded_pharse[:8], 2)]))
                            coded_pharse = coded_pharse[8:]
                else:
                    for word in file_word_list:
                        for letter in word:
                            # Change each symbol to a byte
                            coded_pharse += str(coding_dictionary.get(letter))
                            if len(coded_pharse) >= 8:
                                f.write(bytearray([int(coded_pharse[:8], 2)]))
                                coded_pharse = coded_pharse[8:]
                # Check if the remain of the last byte is 8 bits
                if (8 - (len(coded_pharse) % 8)) > 0 and (8 - (len(coded_pharse) % 8)) < 8:
                    complete_to_byte = (8 - (len(coded_pharse) % 8)) * '0'
                    byte_data = str(format((8 - (len(coded_pharse) % 8)), '08b'))
                else:
                    complete_to_byte = ''
                    byte_data = '00000000'
                coded_pharse += complete_to_byte
                coded_pharse = [coded_pharse[i:i + 8] for i in range(0, len(coded_pharse), 8)]
                # Add the two last bytes to the compressed file
                count = 0
                for i in coded_pharse:
                    coded_pharse[count] = int(i, 2)
                    count += 1
                arr = bytearray(coded_pharse)
                f.write(arr)
            with open(compressed_file_path, 'rb+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write((bytearray([int(byte_data[:8], 2)]))+content)

        self.input_file_path = input_file_path
        self.given_file_type = file_type_of_given_file_to_compress(self.input_file_path)
        self.dir_path = os.path.dirname(self.input_file_path)
        self.word_dictionary = {}
        self.file_word_list = []
        [self.word_dictionary, self.file_word_list] = create_word_dictionary(self.word_dictionary, self.file_word_list)
        self.word_dictionary_list = sorted(self.word_dictionary.items(), key=lambda x: x[1])
        self.min_frequency_of_symbol = self.word_dictionary_list[0]
        self.coding_dictionary = {}
        self.binary_frequency_dictionary = {}
        self.compressed_file_path = os.path.join(self.dir_path, 'compressed_file.bin')
        # Create the tree from the element until creating the root
        if self.given_file_type == 'bin':
            while len(self.word_dictionary_list) > 1:
                self.node_tree = tree_build_bin(self.word_dictionary_list)
                # Sort the element list for lowest frequency at the beginning
                self.word_dictionary_list = sorted(self.word_dictionary_list, key=lambda x: x[1])
        else:
            while len(self.word_dictionary_list) > 1:
                self.node_tree = tree_build_txt(self.word_dictionary_list)
                # Sort the element list for lowest frequency at the beginning
                self.word_dictionary_list = sorted(self.word_dictionary_list, key=lambda x: x[1])
        self.coding_dictionary = create_word_binary_dictionary(self.word_dictionary_list, self.coding_dictionary)
        self.max_length_of_binary_symbol = len(self.coding_dictionary.get(self.min_frequency_of_symbol[0]))
        # Create the compressed file
        create_compressed_file(self.compressed_file_path, self.file_word_list, self.coding_dictionary,
                               self.given_file_type)

    def decompress_file(self, input_file_path):
        """ An method of the class for decompressing the files.

       :param input_file_path: The path of the compressed file.
       :rtype: A: A path of the decompressed file path as string."""
        def check_type_of_file_from_binary_compressed_code(input_file_path):
            """ Check the type of the file before the compression.

           :param input_file_path: The path of the compressed file.
           :rtype: A: A path of the decompressed file path as string with the extension of the target file as string."""
            decompressed_file_path = os.path.join(os.path.dirname(input_file_path), ('decompressed_file.' + self.given_file_type))
            return decompressed_file_path

        def extract_binary_string_from_file_and_create_decompress_file(input_file_path, decompress_file_path, max_length_of_binary_symbol):
            """ An method of the class for decompressing the files.

           :param input_file_path: The path of the compressed file.
           :param decompress_file_path: The path for the decompressed file.
           :param max_length_of_binary_symbol: split the binary string in each conversion to minimal length of one binary symbol."""
            # Read the compressed file
            with open(input_file_path, 'rb') as file:
                file_word_string = file.read()
            binary_string = ''
            # Check the type the target file
            if decompress_file_path.endswith('.bin'):
                permission = 'wb'
            else:
                permission = 'w+'
            # Write to the decompressed file
            with open(decompress_file_path, permission) as file:
                # Converting bytes to symbols without file data symbol
                for binary_number in file_word_string[1:-1]:
                    binary_string += format(binary_number, '08b')
                    if len(binary_string) > max_length_of_binary_symbol*3:
                        element_string = []
                        while len(binary_string) > max_length_of_binary_symbol*2:
                            [element_string, binary_string] = create_element_string_from_binary_string(binary_string,
                                                                                                       element_string)
                        if permission == 'wb':
                            file.write(bytearray(element_string))
                        else:
                            file.write(''.join(element_string))
                data_byte = format(file_word_string[0], '08b')
                last_byte = remove_extra_bits_from_compressing((format(file_word_string[-1], '08b')), data_byte)
                binary_string += last_byte
                element_string = []
                while len(binary_string) > 0:
                    [element_string, binary_string] = create_element_string_from_binary_string(binary_string,
                                                                                               element_string)
                if permission == 'wb':
                    file.write(bytearray(element_string))
                else:
                    file.write(''.join(element_string))

            return binary_string

        def remove_extra_bits_from_compressing(binary_string, data_byte):
            """ Remove the bits for completing to a byte.

           :param data_byte: The number of the extra bits.
           :param binary_string: The string with the extra bits.
           :rtype: A: The string without the extra bits as string."""
            bits_to_remove = int(data_byte, 2)
            if bits_to_remove != 0:
                binary_string = binary_string[:-bits_to_remove]
            return binary_string

        def create_element_string_from_binary_string(binary_string, element_string_list):
            """ Converting binary string to element list.

           :param binary_string: The string for converting.
           :param element_string_list: Empty list for symbols
           :rtype: A: A list of symbols as list.
           :rtype: B: The remain of the not converted binary string as string."""
            binary_string = list(binary_string)
            # Search the symbols with the Node methods
            [element_string_list, binary_string] = self.node_tree.binary_to_element_string(binary_string,
                                                                                           element_string_list)
            return [element_string_list, binary_string]

        self.decompress_file_path = check_type_of_file_from_binary_compressed_code(input_file_path)
        extract_binary_string_from_file_and_create_decompress_file(input_file_path, self.decompress_file_path, self.max_length_of_binary_symbol)

        return self.decompress_file_path

    def calculate_entropy(self):
        """ An method of the class for calculating the entropy of the target file.

       :rtype: A: The entropy of the target file as float."""
        # Number of total symbols in the target file
        total_symbols = self.node_tree.frequency
        entropy = 0.0
        # Frequency of each symbol in relative to the total number of symbol
        for freq in self.word_dictionary.values():
            entropy += (freq / total_symbols) * math.log((freq / total_symbols), 2)
        return -entropy


class Node:
    """ Create a Node between to symbols """

    def __init__(self, element_1, element_2):
        """ Create the node with two elements connected

        :param element_1: A Node or symbol.
        :param element_2: A Node or symbol."""

        self.left = element_1
        self.right = element_2
        self.data = None
        self.frequency = None
        self.leaf = False
        self.binary_frequency = ''

    def search_element(self, dictionary):
        """ Search an symbol in the tree and create dictionary with the binary path to each symbol.

        :param dictionary: An empty dictionary.
        :rtype: A: The dictionary of tree with keys as strings or integers and values as strings."""
        # Check if the node is a leaf
        if self.leaf is True:
            # Create a dictionary value
            dictionary[self.data] = self.binary_frequency
            return dictionary
        else:
            # Recursive search of element in the tree
            self.left.binary_frequency = self.binary_frequency + '0'
            self.left.search_element(dictionary)
            self.right.binary_frequency = self.binary_frequency + '1'
            self.right.search_element(dictionary)

    def binary_to_element_string(self, binary_string, element_string):
        """ Search an symbol in the tree and create a list of the symbols converted from the binary path.

        :param binary_string: Binary string for going through the binary path in the tree.
        :param element_string: An empty list for the symbols
        :rtype: A: The element list with the converted as list."""

        # Check if the node is a leaf == a symbol
        if self.leaf is True:
            element_string.append(self.data)
        else:
            # If not, preform recursive method
            if binary_string[0] == '0':
                binary_string.pop(0)
                self.left.binary_to_element_string(binary_string, element_string)
            else:
                binary_string.pop(0)
                self.right.binary_to_element_string(binary_string, element_string)
        return [element_string, binary_string]


if __name__ == '__main__':
    import time

    start = time.time()
    check = HuffmanCoding('C:\\Users\\ophir\\PycharmProjects\\Homework_3\\bible.txt')
    print(check.calculate_entropy())
    print(check.decompress_file('C:\\Users\\ophir\\PycharmProjects\\Homework_3\\compressed_file.bin'))
    if ((check.calculate_entropy()) * (os.path.getsize(check.input_file_path)) / 8) < os.path.getsize(
            check.compressed_file_path) and os.path.getsize(check.compressed_file_path) < (
            (check.calculate_entropy() + 1) * (os.path.getsize(check.input_file_path)) / 8):
        print("The compression is ok")
    elif os.path.getsize(check.compressed_file_path) < (
            (check.calculate_entropy() + 1) * (os.path.getsize(check.input_file_path)) / 8):
        print("The compression is excellent")
    else:
        print("The compression is bad!!!")
    print(os.path.getsize(check.compressed_file_path))
    end = time.time()
    print('The final time is: ' + str(end - start))
