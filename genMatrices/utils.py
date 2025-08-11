import numpy as np


def SaveMatrix_csv (F, output_file_path):

    with open(output_file_path, 'w') as f:
        # Write the size
        size = np.shape(F)[0]
        f.write(f"{size}\n")
        
        # Write an empty line
        f.write("\n")
        
        # Write the matrix
        for row in F:
            line = "\t".join(map(str, row))
            f.write(f"{line}\n")
    