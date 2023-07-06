import stac
import bidict


def _toric_codes_syndrome_measurements(rows, cols):
    '''
    This function creates a syndrome measurement circuit for the Toric Code of any dimension. 
    Parameters
    -----------
    cols : The number of qubits in a horizontal line. 
    
    rows : The number of qubits in a vertical line.
        
    Returns    stac.Circuit with appended gates
    '''

    #Base Case
    if rows < 2 or cols < 2:
        print("The number of rows and columns should be greater than 2")
        return None
    elif rows%2 !=0 or cols%2 !=0:
        print("The number of rows and columns must be even")
        return None
    

    # Initialize a stac.Circuit object to represent the Toric Code circuit
    toric_code_circ = stac.Circuit()
    
    num_qubits = rows * cols

    # In the Toric Code, the number of data points and syndrome points is always equal to half the total number of qubits
    num_data_qubits = num_syndrome_qubits = num_qubits // 2

    # Append two stac.QubitRegister objects to the circuit, one for data points and one for syndrome points
    toric_code_circ.append_register(stac.QubitRegister('d', 0, num_data_qubits))
    toric_code_circ.append_register(stac.QubitRegister('s', 0, num_syndrome_qubits))

    # Assign coordinates to the physical register elements of the circuit
    toric_code_circ.physical_register.elements = [stac.PhysicalQubit(cols*i+j, (j, i), []) for i in range(rows) for j in range(cols)]

    # Initialize the layout map of the circuit using a bidirectional dictionary
    toric_code_circ.layout_map = bidict.bidict()

    # Initialize counters for data and syndrome points
    d_i = 0
    s_i = 0

    # Iterate over the rows and columns of the circuit to assign data and syndrome points to their respective registers
    for i in range(rows):
        if i % 2 == 0:
            for j in range(cols):
                if j % 2 != 0:
                    toric_code_circ.register[(0,0, d_i)].constituent_register = toric_code_circ.physical_register.elements[cols*i+j]
                    toric_code_circ.layout_map[(0,0,d_i)] = (j, i)
                    d_i += 1

                else:
                    toric_code_circ.register[(0,1,s_i)].constituent_register = toric_code_circ.physical_register.elements[cols*i+j]
                    toric_code_circ.layout_map[(0,1,s_i)] = (j, i)
                    s_i += 1

        else:
            for j in range(cols):
                if j % 2 == 0:
                    toric_code_circ.register[(0,0, d_i)].constituent_register = toric_code_circ.physical_register.elements[cols*i+j]
                    toric_code_circ.layout_map[(0,0,d_i)] = (j, i)
                    d_i += 1

                else:
                    toric_code_circ.register[(0,1,s_i)].constituent_register = toric_code_circ.physical_register.elements[cols*i+j]
                    toric_code_circ.layout_map[(0,1,s_i)] = (j, i)
                    s_i += 1

    # Clear the circuit to remove any gates that may have been added during initialization
    toric_code_circ.clear()

    # Iterate over the syndrome qubits to take syndrome measurements
    for qubit in toric_code_circ.register[(0,1)].qubits():

        # Coordinates of the syndrome qubit
        s_coordinate = qubit.constituent_register.coordinates

        # Calculate the coordinates of neighboring data qubits to wrap around the edges of the lattice
        d_1 = (qubit.constituent_register.coordinates[0], (qubit.constituent_register.coordinates[1]+1) % rows)
        d_2 = ((qubit.constituent_register.coordinates[0]-1) % cols, qubit.constituent_register.coordinates[1])
        d_3 = ((qubit.constituent_register.coordinates[0]+1) % cols, qubit.constituent_register.coordinates[1])
        d_4 = (qubit.constituent_register.coordinates[0], (qubit.constituent_register.coordinates[1]-1) % rows)

        if s_coordinate[1] % 2 == 0: #Z Stabilizer
            # Apply CX gates between the syndrome qubit and its neighboring data qubits in the north, south, east, and west directions
            for i in [d_1, d_2, d_3, d_4]:
                toric_code_circ.geo_append('CX', i, s_coordinate)
            # Apply a TICK gate to advance the circuit to the next time step
            toric_code_circ.geo_append('TICK')

        else: #X Stabilizer
            # Apply H gate to syndrome qubit, CX from neighbors to syndrome, apply H to syndrome qubits again.
            toric_code_circ.geo_append('H', s_coordinate)

            for i in [d_1, d_2, d_3, d_4]:
                toric_code_circ.geo_append('CX', s_coordinate, i)

            toric_code_circ.geo_append('H', s_coordinate)
            toric_code_circ.geo_append('TICK')

    return toric_code_circ






