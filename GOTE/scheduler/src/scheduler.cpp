#include "scheduler.h"

Scheduler *Scheduler::_p_instance = nullptr;
SchedulerDestroyer Scheduler::_destroyer;

// ----------------------------------------------------------------------------
void SchedulerDestroyer::initialize(Scheduler *p) { p_instance = p; }

SchedulerDestroyer::~SchedulerDestroyer() { delete p_instance; }

// ----------------------------------------------------------------------------
Scheduler &Scheduler::getInstance() {
  if (!_p_instance) {
    _p_instance = new Scheduler();
    _destroyer.initialize(_p_instance);
  }
  return *_p_instance;
}

Scheduler::Scheduler() {
  std::
}