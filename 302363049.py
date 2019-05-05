import Huffman_code_interface
from functools import total_ordering
import os
import math




class HuffmanCoding(Huffman_code_interface.HuffmanCoding):  # This is the way you construct a class that inherits properties

    def __init__(self, input_file_path):

        class Node:

            def __init__(self, element_1, element_2):
                self.left = element_1
                self.right = element_2
                self.data = None
                self.frequency = None
                self.leaf = False
                self.binary_frequency = ''

            def search_element(self):
                if self.leaf is True:
                    # print(self.data, self.binary_frequency)
                    letter_binary_frequency = (self.data, self.binary_frequency)
                    return letter_binary_frequency
                else:
                    self.left.binary_frequency = self.binary_frequency + '0'
                    self.left.search_element()
                    self.right.binary_frequency = self.binary_frequency + '1'
                    self.right.search_element()


        def file_type_of_given_file_to_compress(path_of_file):
            """ Check type of file: Bin or Text"""
            if path_of_file.endswith('.bin'):
                type = "Bin"
            elif path_of_file.endswith('.txt'):
                type = "Txt"
            else:
                raise TypeError('This is not Text file or Bin file')
            return type

        def create_word_dictionary():
            """ Create a dictionary of the frequency of every letter or byte in a file.
           :param file_path: A string of the file path
           :rtype: A: dictionary"""
            if self.given_file_type == "Bin":
                with open(self.input_file_path, 'rb') as file:
                    file_word_string = file.read()
                for binary_number in file_word_string:
                    if binary_number in self.word_dictionary:
                        self.word_dictionary[binary_number] += 1
                    else:
                        self.word_dictionary[binary_number] = 1
            else:
                with open(self.input_file_path, 'r') as file:
                    file_word_list = file.readlines()
                for word in file_word_list:
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

        def create_word_binary_dictionary(trie, dictionary):
            letter_binary_frequency = (trie[0][0].search_element())
            print(letter_binary_frequency)
            # dictionary[letter_binary_frequency[0][0]] = letter_binary_frequency[0][1]

        self.input_file_path = input_file_path
        self.given_file_type = file_type_of_given_file_to_compress(self.input_file_path)
        self.compressed_file_path = None
        self.dir_path = os.path.dirname(self.input_file_path)
        self.word_dictionary = {}
        self.word_dictionary = create_word_dictionary()
        self.word_dictionary_list = sorted(self.word_dictionary.items(), key=lambda x: x[1])
        self.coding_dictionary = {}
        self.binary_frequency_dictionary = {}

        while len(self.word_dictionary_list) > 1:
            self.node = tree_build(self.word_dictionary_list)
            self.word_dictionary_list = sorted(self.word_dictionary_list, key=lambda x: x[1])

        print(create_word_binary_dictionary(self.word_dictionary_list,self.binary_frequency_dictionary))


    def decompress_file(self, input_file_path):
        pass

    def calculate_entropy(self):
        pass


if __name__ == '__main__':
    check = HuffmanCoding('C:\\Users\\ophir\\PycharmProjects\\Homework_3\\New Text Document.txt')
    # check1 = HuffmanCoding('C:\\Users\\ophir\\PycharmProjects\\Homework_3\\geo.bin')




