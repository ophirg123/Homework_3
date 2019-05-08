import Huffman_code_interface
from functools import total_ordering
import os
import math




class HuffmanCoding(Huffman_code_interface.HuffmanCoding):  # This is the way you construct a class that inherits properties

    def __init__(self, input_file_path):

        def file_type_of_given_file_to_compress(path_of_file):
            """ Check type of file: Bin or Text"""
            if path_of_file.endswith('.bin'):
                type = "bin"
            elif path_of_file.endswith('.txt'):
                type = "txt"
            else:
                raise TypeError('This is not Text file or Bin file')
            return type

        def create_word_dictionary():
            """ Create a dictionary of the frequency of every letter or byte in a file.
           :param file_path: A string of the file path
           :rtype: A: dictionary"""
            if self.given_file_type == "bin":
                with open(self.input_file_path, 'rb') as file:
                    self.file_word_string = file.read()
                for binary_number in self.file_word_string:
                    if binary_number in self.word_dictionary:
                        self.word_dictionary[binary_number] += 1
                    else:
                        self.word_dictionary[binary_number] = 1
            else:
                with open(self.input_file_path, 'r') as file:
                    self.file_word_list = file.readlines()
                for word in self.file_word_list:
                    for l in word:
                        if l in self.word_dictionary:
                            self.word_dictionary[l] += 1
                        else:
                            self.word_dictionary[l] = 1
            return self.word_dictionary

        def tree_build(elements_list):

            if type(elements_list[0][0]) == str or type(elements_list[1][0]) == str:
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
            elements_list.append((node, node.frequency))
            elements_list.pop(0), elements_list.pop(0)
            return node

        def create_word_binary_dictionary(trie, coding_dictionary):
            trie[0][0].search_element(coding_dictionary)
            return self.coding_dictionary

        def create_compressed_file(compressed_file_path, file_word_list, coding_dictionary):
            with open(compressed_file_path, 'wb') as f:
                coded_pharse = ''
                for word in file_word_list:
                    for l in word:
                        coded_pharse += str(coding_dictionary.get(l))
                if (8-(len(coded_pharse) % 8)) > 0:
                    complete_to_byte = (8-(len(coded_pharse) % 8))*'0'
                if self.given_file_type == "bin":
                    file_data_byte = "0000"+"0"+str(format((8-(len(coded_pharse) % 8)), '03'))
                else:
                    file_data_byte = "0000" + "1" + str(format((8-(len(coded_pharse) % 8)), '03'))
                coded_pharse += complete_to_byte + file_data_byte
                coded_pharse = [coded_pharse[i:i + 8] for i in range(0, len(coded_pharse), 8)]
                count = 0
                for i in coded_pharse:
                    coded_pharse[count] = int(i, 2)
                    count += 1
                arr = bytearray(coded_pharse)
                f.write(arr)


        self.input_file_path = input_file_path
        self.given_file_type = file_type_of_given_file_to_compress(self.input_file_path)
        self.dir_path = os.path.dirname(self.input_file_path)
        self.word_dictionary = {}
        self.word_dictionary = create_word_dictionary()
        self.word_dictionary_list = sorted(self.word_dictionary.items(), key=lambda x: x[1])
        self.coding_dictionary = {}
        self.binary_frequency_dictionary = {}
        self.compressed_file_path = self.dir_path+'\compressed_file.bin'

        while len(self.word_dictionary_list) > 1:
            self.node_tree = tree_build(self.word_dictionary_list)
            self.word_dictionary_list = sorted(self.word_dictionary_list, key=lambda x: x[1])

        self.coding_dictionary = create_word_binary_dictionary(self.word_dictionary_list, self.coding_dictionary)

        create_compressed_file(self.compressed_file_path, self.file_word_list, self.coding_dictionary)

    def decompress_file(self, input_file_path):

        def check_type_of_file_from_binary_compressed_code(binary_string, input_file_path):
            if binary_string[-4:-3] == '0':
                type_of_file = 'bin'
            else:
                type_of_file = 'txt'
            decompressed_file_path = os.path.dirname(input_file_path) + '\decompressed_file.'+ type_of_file
            return decompressed_file_path

        def write_to_decompressed_file(decompressed_path, element_string):
            with open(decompressed_path, 'w+') as file:
                print(element_string)
                file.write(element_string)

        with open(input_file_path, 'rb') as file:
            file_word_string = file.read()
        binary_string = ''
        for binary_number in file_word_string:
            binary_string += format(binary_number, '08b')

        self.decompress_file_path = check_type_of_file_from_binary_compressed_code(binary_string, input_file_path)
        bits_to_remove = int(binary_string[-3:], 2)
        binary_string = binary_string[:-8-bits_to_remove]

        element_string_list = []
        binary_string = list(binary_string)
        while len(binary_string) > 0:
            element_string_list = self.node_tree.binary_to_element_string(binary_string, element_string_list)
        element_string = ''
        element_string.join(element_string_list)
        print(element_string)

        write_to_decompressed_file(self.decompress_file_path, element_string)



    def calculate_entropy(self):
        pass


class Node:

    def __init__(self, element_1, element_2):
        self.left = element_1
        self.right = element_2
        self.data = None
        self.frequency = None
        self.leaf = False
        self.binary_frequency = ''

    def search_element(self, dictionary):
        if self.leaf is True:
            dictionary[self.data] = self.binary_frequency
            return dictionary
        else:
            self.left.binary_frequency = self.binary_frequency + '0'
            self.left.search_element(dictionary)
            self.right.binary_frequency = self.binary_frequency + '1'
            self.right.search_element(dictionary)

    def binary_to_element_string(self, binary_string, element_string):

        if self.leaf is True:
            element_string.append(self.data)
        else:
            if binary_string[0] == '0':
                binary_string.pop(0)
                self.left.binary_to_element_string(binary_string, element_string)
            else:
                binary_string.pop(0)
                self.right.binary_to_element_string(binary_string, element_string)
        return element_string

if __name__ == '__main__':
    import time
    start = time.time()
    check = HuffmanCoding('C:\\Users\\ophir\\PycharmProjects\\Homework_3\\New Text Document.txt')
    # check1 = HuffmanCoding('C:\\Users\\ophir\\PycharmProjects\\Homework_3\\bible.txt')
    check.decompress_file('C:\\Users\\ophir\\PycharmProjects\\Homework_3\\compressed_file.bin')
    end = time.time()
    print(end-start)




