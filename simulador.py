#!/usr/bin/python3
# correr como $./simulador programa.txt cintas.txt
from sys import argv

# cintas = entradas
# programa = instrucciones

def process_program(filename):
    # q = estado actual
    # a = simbolo actual
    # x = extraer
    # y = insertar
    # n = nuevo estado
    d = {}
    F = set()
    af = ''

    with open(filename) as program:
        for line in program:
            elements = line.split()

            # automata finito
            if len(elements) == 3:
                q, a, n = line.split()

                # estado final
                if '*' in q:
                    q = q.strip('*')
                    F.add(q)

                d[q, a] = n

            # automata de pila
            elif len(elements) == 5:
                q, a, x, y, n = line.split()

                # estado final
                if '*' in n:
                    n = n.strip('*')
                    F.add(n)

                if '*' in q and not F:
                    q = q.strip('*')
                    F.add(q)

                d[q, a] = (n, x, y)

    # validar que el diccionario no este vacio            
    if d:
        first_value = list(d.values())[0]
        af = 'afd' if len(first_value) == 2 else 'afp'

    return d, F, af

def AFD(d, q0, F, tape):
    q = q0
    
    for symbol in tape:
        q = d[q, symbol]
        
    return q in F

def AFP(d, q0, F, tape):
    stack = ['Z']
    q = q0

    for symbol in tape:
        q, pop_item, push_item = d[q, symbol]

        if push_item != 'λ' and push_item != '_':
            stack.append(push_item)
            
        if pop_item != 'λ' and pop_item != '_':
            for i, item in enumerate(stack):
                if item == pop_item:
                    stack.pop(i)
                    break

    print(list(reversed(stack)))

    if not F:
        return len(stack) == 0
    else:
        return q in F

def process_tapes(filename, d, F, af):
    message = {True: 'Aceptada', False: 'Rechazada'}
    
    with open(filename) as tapes:
        for tape in tapes:
            tape = tape.strip()
            result = ''
            
            if af == 'afd':
                result = message[AFD(d, '0', F, tape)]
            elif af == 'afp':
                result = message[AFP(d, '0', F, tape)]
            
            print(f'Entrada {tape} es {result}')

if __name__ == '__main__':
    program = argv[1] 
    tapes = argv[2]
    
    d, F, af = process_program(program)
    process_tapes(tapes, d, F, af)

        
