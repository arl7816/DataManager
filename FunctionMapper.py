from DataPoint import Data
from Plot import *
from random import random, randint
from math import e, pow, log, sqrt

class Mapper:

  def __init__(self, dataset: Data, model: object, partials: list, coes: list) -> None:
    self.dataset = dataset
    self.model = model
    self.partials = partials
    self.coes = coes
    
    return

  @staticmethod
  def nudge():
    num = random() * 10
    if (randint(0,1) == 1):
      num *= -1

    return num

  def use_function(self, x: float) -> float:
    n = len(self.coes)
    sigma = 0
    for i in range(n):
      sigma += self.coes[i] * pow(x, i)
    return sigma
  
  def generate_predictions(self, x_values: list) -> Data:
    return Data((x_values, [self.model(x, self.coes) for x in x_values]))

  def generate_function_v1(self, alpha = .1, iterations = 100_000, k_values = 100, bounds = (-100, 100), print_me=False) -> list:
    def gradient(partial: object) -> float:
      sigma = 0
      n = len(self.dataset.x)
      for index in range(n):
        sigma += partial(self.dataset.x[index], self.dataset.y[index], self.coes)

      return sigma / (n-1)
    
    def generate_coes(coes: list, iterations: int) -> list:
      for _ in range(iterations):
        for i in range(len(self.coes)):
          self.coes[i] = self.coes[i] - alpha * gradient(self.partials[i])
      return self.coes

    best_coes = generate_coes(self.coes, iterations)
    for _ in range(k_values):
      temp_coes = [randint(bounds[0], bounds[1]) for n in range(len(self.coes))]
      temp_coes = generate_coes(temp_coes, iterations)

      if self.dataset.standard_error_average(Data((self.dataset.x, [self.model(x, best_coes) for x in self.dataset.x]))) > self.dataset.standard_error_average(Data((self.dataset.x, [self.model(x, temp_coes) for x in self.dataset.x]))):
        best_coes = temp_coes
      if print_me:
        print(best_coes, "produced error at", self.dataset.standard_error_average(Data((self.dataset.x, [self.model(x, best_coes) for x in self.dataset.x]))), "with a alhpa of", alpha)
    self.coes = best_coes
    return best_coes
      

  """def generate_function_v2(dataset: Data, model: object ,partials: list, coes: list, alpha = .1, iterations = 100_000, k_values = 100, bounds = (-100, 100), print_me=False) -> list:
    def gradient(dataset: Data, model: object, partial: object, coes: list) -> float:
      sigma = 0
      demo_sigma = 0
      n = len(dataset.x)
      for index in range(n):
        sigma += partial(dataset.x[index], dataset.y[index], coes)
        demo_sigma += pow(dataset.y[index] - model(dataset.x[index], coes), 2)

      return sigma / (2 * sqrt(demo_sigma * n))

    def generate_coes(self, dataset: Data, model: object, partial: object, coes: list, iterations: int) -> list:
      for _ in range(iterations):
        for i in range(len(coes)):
          coes[i] = coes[i] - alpha * gradient(dataset, model, partial[i], coes)
      return coes

    best_coes = generate_coes(dataset, model, partials, coes, iterations)
    for _ in range(k_values):
      temp_coes = [randint(bounds[0], bounds[1]) for n in range(len(coes))]
      temp_coes = generate_coes(dataset, model, partials, temp_coes, iterations)

      if Mapper.standard_error_average(dataset, Data((dataset.x, [base_test(x, best_coes) for x in dataset.x]))) > self.standard_error_average(dataset, Data((dataset.x, [base_test(x, temp_coes) for x in dataset.x]))):
        best_coes = temp_coes
      if print_me:
        print(best_coes, "produced error at", self.standard_error_average(dataset, Data((dataset.x, [base_test(x, best_coes) for x in dataset.x]))), "with a alhpa of", alpha)
    return best_coes"""