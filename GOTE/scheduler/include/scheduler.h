#pragma once
#include "calculation_tasks.h"
#include <queue>

class Scheduler;

class SchedulerDestroyer {
private:
  Scheduler *p_instance;

public:
  ~SchedulerDestroyer();
  void initialize(Scheduler *p);
};

/***
 * @brief Scheduler for task execution. Blocking queue and operations for now
 */
class Scheduler {
public:
  Scheduler(const Scheduler &) = delete;
  Scheduler(const Scheduler &&) = delete;
  Scheduler &operator=(Scheduler &) = delete;
  Scheduler &&operator=(Scheduler &&) = delete;
  static Scheduler &getInstance();

  void addTask(const CalculationTask& task);

  // TODO Implement non-blocking implementation
  /**
   * @brief Execute all task from queue
   */
  void runTasks();

private:
  std::queue<CalculationTask> tasks;

  static Scheduler *_p_instance;
  static SchedulerDestroyer _destroyer;

protected:
  Scheduler();
  ~Scheduler() = default;
  friend class SchedulerDestroyer;
};
