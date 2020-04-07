#pragma once
#include <map>
#include <string>
#include <vector>

/**
 * @brief Represent connector to remote/virtual ssh host. Stupid asf
 */
class Bridge {
public:
  /**
   * @brief Execute command on specified
   * @return std::string is just a container, data can be in different format
   */
   virtual std::vector<std::string> runCommand(const std::string& command) = 0;
   bool isBusy() const { return _isBusy; }

private:
  bool _isBusy = false;
};

// ----------------------------------------------------------------------------
/**
 * @brief Reuse implemented python bridge
 */
class PythonBridge: public Bridge {
public:
  explicit PythonBridge(const std::string &pathToPythonBridge)
      : _pathToExecutable(pathToPythonBridge) {}

  std::vector<std::string> runCommand(const std::string &command) override;;

private:
  std::string _pathToExecutable;
};

// ----------------------------------------------------------------------------
std::vector<std::string> PythonBridge::runCommand(const std::string &command) {
  // TODO Run command.
}
