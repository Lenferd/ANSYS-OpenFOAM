#pragma once

#include "macros.h"
#include "problem_interface.h"
#include <string>

class TStronginC3Problem : public IProblem {
protected:
  int mDimension;
  bool mIsInitialized;
  static const int mSupportedDimension = 2;

public:
  TStronginC3Problem();
  virtual int SetConfigPath(const std::string &configPath) {
    return IProblem::OK;
  }
  virtual int SetDimension(int dimension);
  virtual int GetDimension() const { return mDimension; }
  virtual int Initialize();

  virtual void GetBounds(double *upper, double *lower);
  virtual int GetOptimumValue(double &value) const;
  virtual int GetOptimumPoint(double *x) const;

  virtual int GetNumberOfFunctions() const { return _numberOfFunctions; }
  virtual int GetNumberOfConstraints() const { return _numberOfConstraints; }
  virtual int GetNumberOfCriterions() const { return _numberOfCriterions; }

  virtual double CalculateFunctionals(const double *x, int fNumber);

  ~TStronginC3Problem() = default;

private:
  int _numberOfFunctions;
  int _numberOfConstraints;
  int _numberOfCriterions;
};

EXPORT_API IProblem *create();
EXPORT_API void destroy(IProblem *ptr);
