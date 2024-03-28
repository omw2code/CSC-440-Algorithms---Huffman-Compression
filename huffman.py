import marshal
import os
import pickle
import sys
from array import array
from typing import Dict
from typing import Tuple
from queue import PriorityQueue


def encode(message: bytes) -> Tuple[str, Dict]:
    """ Given the bytes read from a file, encodes the contents using the Huffman encoding algorithm.

    :param message: raw sequence of bytes from a file
    :returns: string of 1s and 0s representing the encoded message
              dict containing the decoder ring as explained in lecture and handout.
    """
    freq = dict()
    
    #iterate through the bytes
    #map frequencies of the bytes
    for b in message:
        if b in freq:
            freq[b] += 1
        else:
            freq[b] = 1

    #sort the bytes
    sorted_freq = sorted(freq.items(), key=lambda kv: kv[1])

    #Invariant: A list of tuples where each tuple represents a node in the Huffman tree. 
    #           The tuples contain either a single byte with its frequency, or a tuple representing 
    #           an internal node with its children, the combined frequency of the children, and the 
    #           depth of the node in the tree.
    #Initialization: At the beginning of the function, sorted_freq is initialized as an empty list.
    #Maintenance: After processing each pair of least frequent nodes and combining them into a new internal 
    #             node, the list sorted_freq is updated with the new internal node.
    sorted_freq = [(x, xf, 0) for (x, xf) in sorted_freq]

    #Invariant: Invariant: During each iteration of the while loop, sorted_freq maintains a list of tuples where 
    #           each tuple represents a node in the Huffman tree. The tuples contain either a single byte with its 
    #           frequency, or a tuple representing an internal node with its children, the combined frequency of the 
    #           children, and the depth of the node in the tree. The list is sorted based on the frequencies in ascending order.
    #Maintenance: Maintenance: After processing each pair of least frequent nodes and combining them into a new internal 
    #             node, the list sorted_freq is updated with the new internal node. The list is then sorted again based 
    #             on frequencies. This process continues until there is only one node left in sorted_freq, representing 
    #             the root of the Huffman tree.
    #Termination: Termination: The loop terminates when there is only one node left in sorted_freq, which represents 
    #             the root of the Huffman tree and indicates the completion of the encoding process.
    while len(sorted_freq) > 1:

        #Take the two least frequent trees (x, y)
        left, right = sorted_freq[:2]

        sorted_freq.remove(left)
        sorted_freq.remove(right)

        #create a tuple
        tup = ((left, right), left[1] + right[1], 1 + max(left[2], right[2]))

        #Insert that tree into the forest
        sorted_freq.append(tup)
        sorted(sorted_freq, key=lambda kv: kv[1])

    tree = sorted_freq[0]

    encoding_dict = dict()
    for character in freq:
        helper(encoding_dict, tree, character, "")
    
    encoded_message = ""
    for character in message:
        encoded_message = encoded_message + encoding_dict[character]
    encoding_dict = dict((v,k) for k,v in encoding_dict.items())
    return (encoded_message, encoding_dict)

def helper(encoding_dict, tree: Tuple[Dict], character, msg):
    #if leaf do something and return
    if tree[2] == 0:
        if tree[0] == character:
            encoding_dict[character] = msg
        return

    #iterate through the left and right tree
    helper(encoding_dict, tree[0][0], character, msg = msg + '0')
    helper(encoding_dict, tree[0][1], character, msg = msg + '1')


    #check left and right until we find that node

def decode(message: str, decoder_ring: Dict) -> bytes:
    """ Given the encoded string and the decoder ring, decodes the message using the Huffman decoding algorithm.

    :param message: string of 1s and 0s representing the encoded message
    :param decoder_ring: dict containing the decoder ring
    return: raw sequence of bytes that represent a decoded file
    """
    decoded_message = []
    current_code = ""
    
    for bit in message:
        current_code += bit
        #check if the current code is in the decoder ring
        if current_code in decoder_ring:
            decoded_message.append(decoder_ring[current_code])
            current_code = ""
    
    decoded_bytes = bytes(decoded_message)
    return decoded_bytes
    


def compress(message: bytes) -> Tuple[array, Dict]:
    """ Given the bytes read from a file, calls encode and turns the string into an array of bytes to be written to disk.

    :param message: raw sequence of bytes from a file
    :returns: array of bytes to be written to disk
              dict containing the decoder ring
    """
    _message, _decoder_ring = encode(message)

    current_byte = 0
    bit_count = 0
    encoded_bytes = array('B')
    

    for bit in _message:
        #add the current bit to the current_byte
        current_byte = (current_byte << 1) | int(bit, 2)
        bit_count += 1
        
        #add the byte to the array
        if bit_count == 8:
            encoded_bytes.append(current_byte)
            current_byte = 0
            bit_count = 0
    
    #if remaining bits pad with zeros and add the byte
    _decoder_ring["padding_len"] = 0
    if bit_count > 0:
        current_byte <<= (8 - bit_count)
        encoded_bytes.append(current_byte)
        _decoder_ring["padding_len"] = 8 - bit_count

    
    return (encoded_bytes, _decoder_ring)


def decompress(message: array, decoder_ring: Dict) -> bytes:
    """ Given a decoder ring and an array of bytes read from a compressed file, turns the array into a string and calls decode.

    :param message: array of bytes read in from a compressed file
    :param decoder_ring: dict containing the decoder ring
    :return: raw sequence of bytes that represent a decompressed file
    """
    #convert array of bytes back into a binary string
    binary_str = ''.join(format(byte, '08b') for byte in message)
    
    #triming binary string to its original length
    binary_str = binary_str[:(len(binary_str) - decoder_ring["padding_len"])]
    
    return decode(binary_str, decoder_ring)


if __name__ == '__main__':
    usage = f'Usage: {sys.argv[0]} [ -c | -d | -v | -w ] infile outfile'
    if len(sys.argv) != 4:
        raise Exception(usage)

    operation = sys.argv[1]
    if operation not in {'-c', '-d', '-v', '-w'}:
        raise Exception(usage)

    infile, outfile = sys.argv[2], sys.argv[3]
    if not os.path.exists(infile):
        raise FileExistsError(f'{infile} does not exist.')

    if operation in {'-c', '-v'}:
        with open(infile, 'rb') as fp:
            _message = fp.read()

        if operation == '-c':
            _message, _decoder_ring = compress(_message)
            with open(outfile, 'wb') as fp:
                marshal.dump((pickle.dumps(_decoder_ring), _message), fp)
        else:
            _message, _decoder_ring = encode(_message)
            print(_message)
            with open(outfile, 'wb') as fp:
                marshal.dump((pickle.dumps(_decoder_ring), _message), fp)

    else:
        with open(infile, 'rb') as fp:
            pickleRick, _message = marshal.load(fp)
            _decoder_ring = pickle.loads(pickleRick)

        if operation == '-d':
            bytes_message = decompress(array('B', _message), _decoder_ring)
        else:
            bytes_message = decode(_message, _decoder_ring)
        with open(outfile, 'wb') as fp:
            fp.write(bytes_message)
