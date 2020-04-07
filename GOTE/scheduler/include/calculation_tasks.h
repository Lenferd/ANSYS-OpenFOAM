#pragma once

#include <map>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

/**
 * @brief Wrapper for one function calculation
 */
class CalculationTask {
public:
  using Ptr = std::shared_ptr<CalculationTask>;

  CalculationTask(const std::string &functionName,
                  const std::vector<double>& valuesToCalculate);

  const std::string &getFunctionName() const { return _functionName; }
  const std::vector<double> &getValues() const { return _values; }
  double getResult() const;;

  double setResult(const double& result);

protected:
  const std::string _functionName;
  const std::vector<double> _values;
  double _result;
  bool _isCalculated = false;

};

// ----------------------------------------------------------------------------
CalculationTask::CalculationTask(const std::string &functionName,
                                 const std::vector<double> &valuesToCalculate)
    : _functionName(functionName), _values(valuesToCalculate) {}

double CalculationTask::setResult(const double &result) {
  _result = result;
  _isCalculated = true;
}

double CalculationTask::getResult() const {
  if (!_isCalculated) {
    throw std::logic_error("Function is not calculated yet");
  }
  return _result;
}
