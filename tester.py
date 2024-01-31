from mathFunctions import *
from Plot import Plotter
from FunctionMapper import Mapper
from DataPoint import Data

def main() -> None:
    x_test = [n for n in range (1,100, 3)]
    y = [f(n) + Mapper.nudge() for n in x_test]

    y2 = [f(n) for n in x_test]

    data = Data((x_test, y))
    best_fit = Data(data.line_of_best_fit())
    perfect = Data((x_test, y2))

    quad = Mapper(data, base_test, [base_test_d_d0, base_test_d_d1, base_test_d_d2], [1,1,1])

    constants = quad.generate_function_v1(.00000001, print_me=False, iterations=10_000, k_values=1)
    print("Trying it out with constants =", constants)
    test = quad.generate_predictions(x_test)

    """ln_constants = generate_function_v1(data, ln_test, [ln_test_d0, ln_test_d1, ln_test_d2], [1,1,1], 0.000001, 10_000, 1)
    print("ln constants =", ln_constants)
    y4 = [ln_test(x, ln_constants) for x in x_test]
    ln_data = Data((x_test, y4))

    trig_constants = generate_function_v1(data, trig_test, [trig_d0, trig_d1, trig_d2, trig_d3, trig_d4], [1,1,1,1,1], 0.000001, 10_000, 1)
    print("trig constants =", trig_constants)
    y5 = [trig_test(x, trig_constants) for x in x_test]
    trig_data = Data((x_test, y5))"""


    plot = Plotter()
    pl = plot.scatter((1,1,1), data, "blue", marker="o", legend="test_cases")
    pl2 = plot.plot((1,1,1), best_fit, "green", legend="best fit " + str(round(data.standard_error_average(best_fit))))
    pl3 = plot.plot((1,1,1), perfect, "red", "perfect " + str(round(data.standard_error_average(perfect))))
    pl4 = plot.plot((1,1,1), test, "purple", "quad " + str(round(data.standard_error_average(test))))
    #pl5 = plot.plot((1,1,1), ln_data, "pink", "ln " + str(round(standard_error_average(data, ln_data))))
    #pl6 = plot.plot((1,1,1), trig_data, "yellow", "trig " + str(round(standard_error_average(data, trig_data))))

    pl.legend()
    pl.grid()

    plot.show()

    return

if __name__ == "__main__":
    main()