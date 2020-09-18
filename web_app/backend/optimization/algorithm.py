from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.problem import ZDT1
from jmetal.util.termination_criterion import StoppingByEvaluations
import cost_functions

class EnergyBuildingMulti(FloatProblem):
    
    def __init__(self, irradiance, demand, N, Ce, Cv, qinit, Cb, Vb, Cp, Vp, xp_min):
        super().__init__()

        self.irradiance =irradiance
        self.demand = demand
        self.N = N
        self.Ce= Ce
        self.Cv= Cv
        self.qinit = qinit
        self.Cb= Cb
        self.Vb= Vb
        self.Cp= Cp
        self.Vp= Vp
        
        # initial parameters
        self.number_of_variables = 2 # decision variables
        self.number_of_objectives = 2 
        self.number_of_constraints = 2
        self.lower_bound = [0,0]#[0.0 for _ in range(number_of_variables)]
        self.upper_bound = [xp_min,300] #[1.0 for _ in range(number_of_variables)]
        
        self.obj_directions = [self.MINIMIZE, self.MINIMIZE] # both objectives should be minimized
        self.obj_labels = ['cost', 'co2'] # objectives' name
              
    def evaluate(self, solution) -> FloatSolution:
        '''
        define the way to evaluate one solution, i.e., calculate the objectives of each solution
        '''
        Xp = solution.variables[0]
        Xb = solution.variables[1]
        f1,f2 = total_cost(Xp,Xb,self.irradiance, self.demand, self.N, self.Ce, self.Cv, self.qinit, self.Cb, self.Vb, self.Cp, self.Vp)
        #print(f'f1 {f1}, f2 {f2}')
        #f1 = self.eval_f1(solution) # calculate the 1st objective
        #f2 = self.eval_f2(solution, f1) # calculate the 2nd objective     
        solution.objectives[0] = f1
        solution.objectives[1] = f2
        
        return solution
    def get_name(self):
        return 'solar_optimum'


def optimal_panels_battery_multi(Ce,Cv,Cp,Cb,Vp,Vb,demand,irradiance,xp_min):
  
  energy_building = EnergyBuildingMulti( irradiance, demand, N, Ce, Cv, qinit, Cb, Vb, Cp, Vp,xp_min)
  algorithm = NSGAII(
      problem=energy_building,
      population_size=100,
      offspring_population_size=100,
      mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
      crossover=SBXCrossover(probability=1.0, distribution_index=20),
      termination_criterion=StoppingByEvaluations(max_evaluations=25000)
  )

  algorithm.run()
  solutions = algorithm.get_result()

  for solution in solutions:
    #print('Solution:',solution.variables, 'Maximum value:',solution.objectives[0])
    Xp = solution.variables[0]
    Xb = solution.variables[1]
    C =  solution.objectives[0]
  print(f'Xp {Xp}, Xb {Xb}, Cost {C}')
  return Xb, Xp, C, algorithm

# parameters initialization
N = 24
Ce = 0.109 # euros/kWh
Cv = 0.054 # euros/kWh
Cp = 800 # euros/m^2
Cb = 128 # euros/kWh
Vp = 20*365  # hours
Vb = 15*365  # hours

# algorithm func call
Xb_opt_multi, Xp_opt_multi, C_opt_multi, algorithm_multi = optimal_panels_battery_multi(Ce,Cv,Cp,Cb,Vp,Vb,demand,irradiance,xp_min=8)