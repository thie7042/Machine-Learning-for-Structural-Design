from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from deap import benchmarks
import numpy as np
import pandas as pd
import time
import openpyxl

# We are setting up the multifunction optimization to minimize our blackbox problems.
# For this trail example, we will use mathematical objective functions

# Lets defined our parameters

# Number of variables
n_var = 5
# NUmber of objectives
n_obj = 2
# Lower Bound for variables
#xl = [-5., -5.]
xl = [400., 200.,200.,100.,100.]
# Upper Bound for variables
xu = [550.,400.,450.,200.,200.]
# Population size
#pop_size = 100
pop_size = 10
# Number of generations
#n_gen = 10
n_gen = 2


# Writing the number of iterations to file
t_file = open('C:/Users/TommyHielscher/Desktop/Abaqus_scripting/ReinforcedTBeam/Parametric/Control/number_of_sols.txt','w')
t_file.write(str(n_gen*pop_size))
t_file.close()



# The problem Wrapper:
def counter():
    print("Counter")

counter.test = 1
counter.all = 1

class ProblemWrapper(Problem):

    def _evaluate(self, designs, out, *args, **kwargs):
        res = []
        sol_counter = 0

        for design in designs:
            #res.append(benchmarks.kursawe(design))
            #print(design)
            #print(benchmarks.kursawe(design))
            #out['F'] = np.array(res)

            sol_counter += 1


            gen_counter = counter.test


            print('Solution: ' + str(sol_counter))
            print("Generation: " + str(gen_counter))
            print(counter.all)

            ###

            var_1 = design[0]
            var_2 = design[1]
            var_3 = design[2]
            var_4 = design[3]
            var_5 = design[4]

            #

            # Change parameter file - Updata input parameters
            f = open("C:/Users/TommyHielscher/Desktop/Abaqus_scripting/ReinforcedTBeam/Parametric/Control/parameters.txt", "w")
            f.write(str(var_1) + "," + str(var_2) + "," + str(var_3) + "," + str(var_4) + "," + str(var_5) + "," + "newdata")
            f.close()

            # Check and read results

            filepath = 'C:/Users/TommyHielscher/Desktop/Abaqus_scripting/ReinforcedTBeam/Parametric/Output/' + 'abaqus_output_' + str(counter.all) + '.txt'
            print(filepath)

            while True:
                time.sleep(0.5)

                try:
                    file = open(filepath, 'r')
                    data = file.read()
                    data = data.split(' ')
                    data = list(filter(None, data))
                    print(data[-2])
                    FEM = float(data[-2])

                except:
                    print('File has not been created. Waiting for analysis. Generation:', gen_counter, " , Solution: ",
                          sol_counter)

                    continue

                break

            print('File found!')


            # For multivariate, this array will contain different results
            results_array = [FEM, FEM]

            res.append(results_array)
            out['F'] = np.array(res)
            ##
            counter.all += 1

            if sol_counter >= pop_size:
                counter.test += 1


problem = ProblemWrapper(n_var=n_var,n_obj=n_obj,xl = xl,xu = xu)


# The Algorithm: NSGA-II

from pymoo.algorithms.moo.nsga2 import NSGA2

algorithm = NSGA2(pop_size=pop_size)

stop_criteria = ('n_gen', n_gen)

results = minimize(
    problem=problem,
    algorithm=algorithm,
    termination=stop_criteria
)

# Pareto Optimal Results
print(results.F)

# Corresponding Parameters
print(results.X)


# Visualizing results

res_data = results.F.T

import plotly.graph_objects as go

fig = go.Figure(data=go.Scatter(x=res_data[0], y= res_data[1], mode='markers'))
fig.show()

#####################


# Exporting Data
arr = results.X
arr2 = results.F.T


df = pd.DataFrame(arr)
df.to_excel("C:/Users/TommyHielscher/Desktop/Abaqus_scripting/ReinforcedTBeam/Parametric/Control/output_data_A.xlsx")

dq = pd.DataFrame(arr2)
dq.to_excel("C:/Users/TommyHielscher/Desktop/Abaqus_scripting/ReinforcedTBeam/Parametric/Control/output_data_B.xlsx")

print(df)


