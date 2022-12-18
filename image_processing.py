# Michael Nguyen 260970685

def is_valid_image(PGM):
    """ (list<list>) -> bool
    Returns if PGM is a valid non-compressed PGM image matrix format.
    
    >>> is_valid_image([["0x5", "200x2"], ["111x7"]])
    False
    >>> is_valid_image([[0],[0]])
    True
    >>> is_valid_image([[1,2,3],[4]])
    False
    """
    if PGM == [[]] or PGM == []:
        return False
    
    length = len(PGM[0])
    
    for row in PGM:
        if len(row) != length:
            return False
        for value in row:
            if type(value) != int or value > 255 or value < 0:
                return False
        
    return True

def is_valid_compressed_image(PGM):
    """ (list<list>) -> bool
    Returns if PGM is a valid compressed PGM image matrix format.
    
    >>> is_valid_compressed_image([["0x5", "200x2"], ["111x7"]])
    True
    >>> is_valid_compressed_image([[0,0],[1,2]])
    False
    >>> is_valid_compressed_image([["0xxx5", "200x2"], ["111x7"]])
    False
    """
    
    if PGM == [[]] or PGM == []:
        return False
    
    Previous_B = 0
    for row in PGM:
        B_values = 0
        for value in row:   
            if type(value) != str or "x" not in value:
                return False
        
            A_B = value.split("x")
            if not A_B[0].isdecimal() or not A_B[-1].isdecimal() \
               or int(A_B[0]) > 255 or int(A_B[0]) < 0 or len(A_B)>2:
                return False
            
            B_values += int(A_B[-1])
        if B_values != Previous_B and row != PGM[0]:
            return False
        
        Previous_B = B_values
    
    return True

def load_regular_image(filename):
    """ (str) -> list<list><int>
    Loads the image from filename and returns the image matrix.
    
    >>> load_regular_image("comp.pgm")
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 187, 187, 187, 187, 0, 255, 255, 255, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 255, 255, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0], [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    >>> image = [[1,2,3],[4,5,6]]
    >>> save_regular_image(image, 'test.pgm')
    >>> load_regular_image('test.pgm')
    [[1, 2, 3], [4, 5, 6]]
    
    >>> file = open('test.pgm', 'w')
    >>> file.write("hello\\nIt\\nis\\nvery")
    16
    >>> file.close()
    >>> load_regular_image('test.pgm')
    Traceback (most recent call last):
    AssertionError: The image file is not in the correct PGM format.
    """
    
    file = open(filename, "r")
    matrix = []
    for line in file:
        line = line.split()
        matrix.append(line)
    matrix = matrix[3:]
    
    for sublist in matrix:
        for values in sublist:
            if not values.isdecimal():
                raise AssertionError("The image file is not in the correct PGM format.")
    
    image_matrix = []
    for i in matrix:
        new_i = []
        for e in i:
            new_i.append(int(e))
        image_matrix.append(new_i)
    
    if matrix == [] or not is_valid_image(image_matrix):
        raise AssertionError("The image file is not in the correct PGM format.")
            
    file.close()        
    return image_matrix
    
def load_compressed_image(filename):
    """ (str) -> list<list><str>
    Loads filename and returns the image matrix.
    
    >>> load_compressed_image("comp.pgm.compressed")
    [['0x24'], ['0x1', '51x5', '0x1', '119x5', '0x1', '187x5', '0x1', '255x4', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x2', '255x1', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x4', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x4'], ['0x1', '51x5', '0x1', '119x5', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x4'], ['0x24']]

    >>> image = [["1x2", "65x3"],["180x5"]]
    >>> save_compressed_image(image, 'test.pgm.compressed')
    >>> load_compressed_image('test.pgm.compressed')
    [['1x2', '65x3'], ['180x5']]
    
    >>> file = open('test.pgm', 'w')
    >>> file.write("1x2\\n2x1 80x1\\n2xx2")
    17
    >>> file.close()
    >>> load_compressed_image('test.pgm')
    Traceback (most recent call last):
    AssertionError: The image file is not in a compressed PGM format.
    """
    
    file = open(filename, 'r')
    image_matrix = []
    for line in file:
        line = line.split()
        image_matrix.append(line)
    image_matrix = image_matrix[3:]
    
    if not is_valid_compressed_image(image_matrix) :
        raise AssertionError("The image file is not in a compressed PGM format.")
    
    file.close()    
    return image_matrix

def load_image(filename):
    """ (str) -> list<list>
    Loads filename and returns the respective image matrix.
    
    >>> load_image("comp.pgm.compressed")
    [['0x24'], ['0x1', '51x5', '0x1', '119x5', '0x1', '187x5', '0x1', '255x4', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x2', '255x1', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x4', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x4'], ['0x1', '51x5', '0x1', '119x5', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x4'], ['0x24']]
    
    >>> image = [["1x2", "65x3"],["180x5"]]
    >>> save_compressed_image(image, 'test.pgm.compressed')
    >>> load_image('test.pgm.compressed')
    [['1x2', '65x3'], ['180x5']]
    
    >>> file = open('test.pgm', 'w')
    >>> file.write("1x2\\n2x1 80x1\\n2xx2")
    17
    >>> file.close()
    >>> load_image('test.pgm')
    Traceback (most recent call last):
    AssertionError: The file is not in a PGM format
    
    """
    
    file = open(filename, 'r')
    for line in file:
        line = line.split()
        if line[0] == "P2":
            return load_regular_image(filename)
        elif line[0] == "P2C":
            return load_compressed_image(filename)
        else:
            raise AssertionError("The file is not in a PGM format")
    
    file.close()
    
def save_regular_image(PGM, filename):
    """ (list<list><int>, str) -> Nonetype
    Takes PGM and saves it into filename in a PGM format.
    
    >>> save_regular_image([[0]*10, [255]*10, [0]*10], "test.pgm")
    >>> fobj = open("test.pgm", 'r')
    >>> fobj.read()
    'P2\\n10 3\\n255\\n0 0 0 0 0 0 0 0 0 0\\n255 255 255 255 255 255 255 255 255 255\\n0 0 0 0 0 0 0 0 0 0\\n'
    >>> fobj.close()
    
    >>> image = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    >>> save_regular_image(image, 'test.pgm')
    
    >>> save_regular_image([[1, 2], [1]], 'test.pgm')
    Traceback (most recent call last):
    AssertionError: Not an appropriate PGM format
    """
    
    if not is_valid_image(PGM):
        raise AssertionError("Not an appropriate PGM format")
    
    file = open(filename, "w")
    file.write("P2\n")
    Dimensions = [str(len(PGM[0])), str(len(PGM))]
    Dimensions = " ".join(Dimensions)
    file.write(Dimensions)
    file.write("\n255")
            
    for i in range (len(PGM)):
        file.write("\n")
        for j in range (len(PGM[i])):
            PGM[i][j] = str(PGM[i][j])
        file.write(" ".join(PGM[i]))

    file.write("\n")
    file.close()
    
def save_compressed_image(PGM, filename):
    """ (list<list><str>, str) -> Nonetype
    Takes PGM and saves it into filename in a PGM format.
    
    >>> save_compressed_image([["0x5", "200x2"], ["111x7"]], "test.pgm.compressed")
    >>> fobj = open("test.pgm.compressed", 'r')
    >>> fobj.read()
    'P2C\\n7 2\\n255\\n0x5 200x2\\n111x7\\n'
    >>> fobj.close()
    
    >>> image = [["0x1", "6x6"], ["123x7"]]
    >>> save_compressed_image(image, "test.pgm.compressed")
    
    >>> save_compressed_image([[1,1],[2,2]], 'test.pgm.compressed')
    Traceback (most recent call last):
    AssertionError: Wrong compressed format
    """
    
    if not is_valid_compressed_image(PGM):
        raise AssertionError("Wrong compressed format")
    
    file = open(filename, "w")
    file.write("P2C\n")
     
    B_values = 0
    for j in PGM[0]:
        individual_values = j.split("x")
        B_values += int(individual_values[-1])
        Dimensions = [str(B_values), str(len(PGM))]
        Dimensions = " ".join(Dimensions)
    file.write(Dimensions)
    file.write("\n255")
    
    for i in PGM:
        i = " ".join(i)
        file.write("\n")
        file.write(i)
        
    file.write("\n")
    file.close()
    
def save_image(PGM, filename):
    """ (list<list>, str) -> Nonetype
    Takes PGM file and depending on the file type, the function will
    either save it as a regular PGM or a compressed PGM.
    
    >>> save_image([["0x5", "200x2"], ["111x7"]], "test.pgm.compressed")
    >>> fobj = open("test.pgm.compressed", 'r')
    >>> fobj.read()
    'P2C\\n7 2\\n255\\n0x5 200x2\\n111x7\\n'
    >>> fobj.close()
    
    >>> save_image([[1,2],[4,5,6]], 'test.pgm.compressed')
    Traceback (most recent call last):
    AssertionError: Not an appropriate PGM format
    
    >>> save_image([[2,3,4], ['1x3']], 'test.pgm.compressed')
    Traceback (most recent call last):
    AssertionError: Inconsistent value type
    """
    
    file = open(filename, "w")
    for i in PGM:
        for j in i:
            value_type = type(j)
            if value_type != type(PGM[0][0]):
                raise AssertionError("Inconsistent value type")
    if value_type == int:
        save_regular_image(PGM, filename)
    elif value_type == str:
        save_compressed_image(PGM,filename)
    else:
        raise AssertionError("Does not follow a PGM format")
    file.close()
        
def invert(PGM):
    """ (list<list><int>) -> list<list><int>
    Takes PGM and returns the inverted image as an image matrix with
    numbers bounded between [0,255].
    
    >>> image = [[0, 100, 150], [200, 200, 200], [255, 255, 255]]
    >>> invert(image)
    [[255, 155, 105], [55, 55, 55], [0, 0, 0]]
    >>> image == [[0, 100, 150], [200, 200, 200], [255, 255, 255]]
    True
    >>> invert([[1,2],[1]])
    Traceback (most recent call last):
    AssertionError: Invalid PGM format
    >>> invert([[100,240,145],[99,98,97],[0,0,0]])
    [[155, 15, 110], [156, 157, 158], [255, 255, 255]]
    """
    
    if not is_valid_image(PGM):
        raise AssertionError("Invalid PGM format")
    
    inverted_PGM = []
    for i in PGM:
        new_i = []
        for n in i:
            n = 255 - n
            new_i.append(n)
        inverted_PGM.append(new_i)
    
    return inverted_PGM
    
def flip_horizontal(PGM):
    """ (list<list><int>) -> list<list><int>
    Takes PGM and returns the horizontally flipped image matrix.
    
    >>> image = [[1, 2, 3, 4, 5], [0, 0, 5, 10, 10], [5, 5, 5, 5, 5]]
    >>> flip_horizontal(image)
    [[5, 4, 3, 2, 1], [10, 10, 5, 0, 0], [5, 5, 5, 5, 5]]
    >>> image == [[1, 2, 3, 4, 5], [0, 0, 5, 10, 10], [5, 5, 5, 5, 5]]
    True
    >>> flip_horizontal([[1,2],[1,2,3]])
    Traceback (most recent call last):
    AssertionError: Invalid PGM format
    >>> flip_horizontal([[1,2,3], [4,5,6]])
    [[3, 2, 1], [6, 5, 4]]
    """
    
    if not is_valid_image(PGM):
        raise AssertionError("Invalid PGM format")
    
    horizontal_flip = []
    for i in range (len(PGM)):
        new_i = []
        for j in range (len(PGM[i]) - 1, -1, -1):
            new_i.append(PGM[i][j])
        horizontal_flip.append(new_i)
    
    return horizontal_flip
        
def flip_vertical(PGM):
    """(list<list><int>) -> list<list><int>
    Takes PGM and returns the vertically flipped image.
    
    >>> image = [[1, 2, 3, 4, 5], [0, 0, 5, 10, 10], [5, 5, 5, 5, 5]]
    >>> flip_vertical(image)
    [[5, 5, 5, 5, 5], [0, 0, 5, 10, 10], [1, 2, 3, 4, 5]]
    >>> image == [[1, 2, 3, 4, 5], [0, 0, 5, 10, 10], [5, 5, 5, 5, 5]]
    True
    >>> flip_vertical([[1,2],[1]])
    Traceback (most recent call last):
    AssertionError: Invalid PGM format
    >>> flip_vertical([[1, 2, 3],[4, 5, 6]])
    [[4, 5, 6], [1, 2, 3]]
    """
    
    if not is_valid_image(PGM):
        raise AssertionError("Invalid PGM format")
    
    vertical_flip = []
    for i in range (len(PGM) - 1, -1, -1):
        vertical_flip.append(PGM[i])
    
    return vertical_flip

def crop(PGM, top_left_row, top_left_column, row, column):
    """ (list<list><int>, int, int, int, int) -> list<list><int>
    Takes PGM and indexes with (top_left_row,top_left_column). Creates
    a matrix starting from those indexes of size row * column.
    
    >>> crop([[5, 5, 5], [5, 6, 6], [6, 6, 7]], 1, 1, 2, 2)
    [[6, 6], [6, 7]]
    >>> crop([[5, 5, 5], [5, 6], [6, 6, 7]], 1, 1, 2, 2)
    Traceback (most recent call last):
    AssertionError: Invalid PGM format
    >>>
"""
    
    if not is_valid_image(PGM):
        raise AssertionError("Invalid PGM format")
    
    cropped_image = []
    cropped_list = []
    cropped_list.append(PGM[top_left_row][top_left_column])
    
    for i in range(1, column):
        cropped_list.append(PGM[top_left_row][top_left_column + i])
    cropped_image.append(cropped_list)
    
    for j in range(1, row):
        cropped_list = []
        for k in range(0, column):
            cropped_list.append(PGM[top_left_row + j][top_left_column + k])
        cropped_image.append(cropped_list)
        
    return cropped_image

def find_end_of_repetition(int_list, index, target):
    """ (list<int>, int, int) -> int
    Takes int_list and returns the last consecutive occurence of target
    starting from index.
    
    >>> find_end_of_repetition([5, 3, 5, 5, 5, -1, 0], 2, 5)
    4
    >>> find_end_of_repetition([5, 3, 5, 5, 5], 0, 5)
    0
    >>> find_end_of_repetition([5, 3, 5, 5, 5, 7], 5, 7)
    5
    """
    
    for i in range(index, len(int_list)):
        if int_list[i] != target:
            return i-1
        
    return i
        
def compress(PGM):
    """ (list<list><int>) -> list<list><str>
    Takes PGM and returns the compressed version of it. If PGM is not a valid
    image, an error message is raised.
    
    >>> compress([[11, 11, 11, 11, 11], [1, 5, 5, 5, 7], [255, 255, 255, 0, 255]])
    [['11x5'], ['1x1', '5x3', '7x1'], ['255x3', '0x1', '255x1']]
    >>> compress([[11,11],[1,2,3],[45,45,45]])
    Traceback (most recent call last):
    AssertionError: Invalid PGM format
    >>> compress([[1,1,1,1,5],[2,2,3,3,3],[4,4,4,4,1]])
    [['1x4', '5x1'], ['2x2', '3x3'], ['4x4', '1x1']]
    """
    
    if not is_valid_image(PGM):
        raise AssertionError("Invalid PGM format")
    
    compressed = []
    for i in range(len(PGM)):
        compressed_values = []
        for j in range(len(PGM[i])):
            values = []
            if PGM[i][j] != PGM[i][j-1] or j == 0:
                target = PGM[i][j]
                values.append(str(target))
                repetition = find_end_of_repetition(PGM[i], j, PGM[i][j]) - j + 1
                values.append(str(repetition))
                values = "x".join(values)
                compressed_values.append(values)
        compressed.append(compressed_values)   
    
    return compressed
            
def decompress(PGM):
    """ (list<list><str>) -> list<list><int>
    Takes PGM, which is a compressed image matrix, and decompresses it.
    If PGM is not a valid compressed matrix, an error messages arises.
    
    >>> decompress([['11x5'], ['1x1', '5x3', '7x1'], ['255x3', '0x1', '255x1']])
    [[11, 11, 11, 11, 11], [1, 5, 5, 5, 7], [255, 255, 255, 0, 255]]
    >>> decompress([['11x5'],['1x1','5x3', '7x2']])
    Traceback (most recent call last):
    AssertionError: Invalid compressed PGM format
    >>> decompress([['1x2'],['2x2'],['3x2']])
    [[1, 1], [2, 2], [3, 3]]
    """
    
    if not is_valid_compressed_image(PGM):
        raise AssertionError("Invalid compressed PGM format")
    
    decompressed = []
    for line in PGM:
        decompressed_values = []
        for char in line:
            char = char.split("x")
            for k in range (int(char[1])):
                decompressed_values.append(int(char[0]))
        decompressed.append(decompressed_values)
    
    return decompressed

def process_command(commands):
    """ (str) -> Nonetype
    Takes commands string and executes individual command value in that string.
    
    >>> process_command("LOAD<comp.pgm> CP DC INV INV SAVE<comp2.pgm>")
    >>> image = load_image("comp.pgm")
    >>> image2 = load_image("comp2.pgm")
    >>> image == image2
    True
    
    >>> load_image('comp.pgm')
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 187, 187, 187, 187, 0, 255, 255, 255, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 255, 255, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0], [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    >>> process_command("LOAD<comp.pgm> INV SAVE<comp2.pgm>")
    >>> load_image('comp2.pgm')
    [[255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255], [255, 204, 204, 204, 204, 204, 255, 136, 136, 136, 136, 136, 255, 68, 68, 68, 68, 68, 255, 0, 0, 0, 0, 255], [255, 204, 255, 255, 255, 255, 255, 136, 255, 255, 255, 136, 255, 68, 255, 68, 255, 68, 255, 0, 255, 255, 0, 255], [255, 204, 255, 255, 255, 255, 255, 136, 255, 255, 255, 136, 255, 68, 255, 68, 255, 68, 255, 0, 0, 0, 0, 255], [255, 204, 255, 255, 255, 255, 255, 136, 255, 255, 255, 136, 255, 68, 255, 68, 255, 68, 255, 0, 255, 255, 255, 255], [255, 204, 204, 204, 204, 204, 255, 136, 136, 136, 136, 136, 255, 68, 255, 68, 255, 68, 255, 0, 255, 255, 255, 255], [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]]
    
    >>> process_command("LOAD<comp.pgm> INV VIN SAVE<comp2.pgm>")
    Traceback (most recent call last):
    AssertionError: Invalid command!
    """
    
    valid_commands = ['LOAD', 'SAVE', 'INV', 'FH', 'FV', 'CR', 'CP', 'DC']
    commands = commands.split(" ")
    
    for command in commands:
        command = command.split("<")
        command[-1] = command[-1].strip(">")
        
        if command[0] not in valid_commands:
            raise AssertionError("Invalid command!")
        
        for i in range (len(command)):
            if command[i] == valid_commands[0] and i == 0:
                image_matrix = load_image(command[1])
            elif command[i] == valid_commands[1] and i == 0 :
                save_image(image_matrix,command[1])
            elif command[i] == valid_commands[2]:
                image_matrix = invert(image_matrix)
            elif command[i] == valid_commands[3]:
                image_matrix = flip_horizontal(image_matrix)
            elif command[i] == valid_commands[4]:
                image_matrix = flip_vertical(image_matrix)
            elif command[i] == valid_commands[5] and i == 0:
                crop_input = command[1].split(",")
                image_matrix = crop(image_matrix, int(crop_input[0]), int(crop_input[1]), \
                                    int(crop_input[2]), int(crop_input[3]))
            elif command[i] == valid_commands[6]:
                image_matrix = compress(image_matrix)
            elif command[i] == valid_commands[7]:
                image_matrix = decompress(image_matrix)
            

            
        