#pragma once

#include <string>

class IProblem
{
public:
    const static int OK = 0;
    const static int ERROR = -1;
    const static int UNDEFINED = -2;

    virtual int SetConfigPath(const std::string& configPath) = 0;
    virtual int SetDimension(int dimension) = 0;
    virtual int GetDimension() const = 0;
    virtual int Initialize() = 0;

    virtual void GetBounds(double* upper, double *lower) = 0;
    virtual int GetOptimumValue(double& value) const = 0;
    virtual int GetOptimumPoint(double* x) const = 0;

    virtual int GetNumberOfFunctions() const = 0;
    virtual int GetNumberOfConstraints() const = 0;
    virtual int GetNumberOfCriterions() const = 0;

    virtual double CalculateFunctionals(const double* x, int fNumber) = 0;
};
