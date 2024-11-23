package backend

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

func ParseString(message string) ([]float64, error) {
	coefs := strings.Fields(message)
	if len(coefs) != 3 {
		return nil, fmt.Errorf("coefficients must be 3 elements (a, b, c)")
	}

	var result []float64
	for _, coef := range coefs {
		floatCoef, err := strconv.ParseFloat(coef, 64)
		if err != nil {
			return nil, err
		}
		result = append(result, floatCoef)
	}
	return result, nil
}

func SolveEquation(a, b, c float64) string {
	if a == 0 {
		return "coef [a] cannot be zero for a quadratic equation"
	}

	switch discriminant := b*b - 4*a*c; {
	case discriminant > 0:
		x1 := (-b + math.Sqrt(discriminant)) / (2 * a)
		x2 := (-b - math.Sqrt(discriminant)) / (2 * a)
		return fmt.Sprintf("x1 = %.2f, x2 = %.2f", x1, x2)
	case discriminant == 0:
		x := -b / (2 * a)
		return fmt.Sprintf("x = %.2f", x)
	default:
		return fmt.Sprintf("no solution, descriminant < 0: D=%.2f", discriminant)
	}
}
