
#Código añadido al fichero
def prepareCircuit(circuit):
    number = int('{{ params.quantumInteger }}') #Numero entero
    qubits = '{{ params.qubitNumber }}' #Numero de qubits del circuito (para codificar el entero a binario)
    littleEndian = '{{ params.littleEndian }}' #Para darle la vuelta si es little endian

    final = format(number,'0'+qubits+'b')

    print(final)

    array = [int(x) for x in str(final)]
    
    if littleEndian == 'true':
        array.reverse()

    count = 0

    #Circuito de entrada
    for x in array:
        if x == 1:
            circuit.x(count) #Para poner un 1
        else:
            circuit.z(count) #Para poner un 0
        count=count+1
    
    return circuit
