
import CNF
import Cnfsolver

global solution
# file = 'Benchmark Problems//uf75-073.cnf'
# file='Benchmark Problems//uf75-067.cnf'
# file='Benchmark Problems//uf75-01.cnf'
# file='Benchmark Problems//uf50-082.cnf'
# file='Benchmark Problems//uf50-050.cnf'
# file='Benchmark Problems//uf50-010.cnf'
# file='Benchmark Problems//uf20-050.cnf'
file='Benchmark Problems//uf20-029.cnf'
# outputfile='Export//uf75-073.txt'
# outputfile='Export//uf75-067.txt'
# outputfile='Export//uf75-01.txt'
# outputfile='Export//uf50-082.txt'
# outputfile='Export//uf50-050.txt'
# outputfile='Export//uf50-010.txt'
# outputfile='Export//uf20-050.txt'
outputfile='Export//uf20-029.txt'
formulas = CNF.readCnf(file)
runner = Cnfsolver.Cnfsolver(formulas)
sum = 0
sumGen = 0
for run in range(0, 20, 1):
    success_rate, solution, generation = runner.solver()
    print('success_rate:', str(success_rate) + '\n', 'solution:', str(solution) + '\n', 'Generation:', generation)
    sum = sum + success_rate
    sumGen = sumGen + generation
avg_success_rate: float = sum / 20
avg_Generation: float = sumGen / 20
print('Average success rate:', avg_success_rate)
f = open(outputfile, 'w+')
f.write('Avg_Generation:%d\r\n' % avg_Generation)
f.write('Avg_success_rate:%d\r\n' % avg_success_rate)
f.write(f'solution:{solution}\r\n')
f.close()
