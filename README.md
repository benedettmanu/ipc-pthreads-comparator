# IPC - Pthreads Comparator

### Introduction

This application counts items on three conveyors and displays the total. One process is responsible for counting and another for the display.

Every 1,500 units processed, the total weight of the items is updated. The conveyors operate as follows:

Belt 1: 5 kg products, 1 item per second.
Belt 2: 2 kg products, 1 item every 0.5 seconds.
Conveyor 3: 0.5 kg products, 1 item every 0.1 second.
Counting is uninterrupted and the display is updated every 2 seconds. The application allows an operator to interrupt the count if necessary.

The implementation uses Pthreads and IPC between piped processes. In the process that uses threads, a mutex or semaphore is used to control access to critical sections.

### Development Environment

```
- Python 3.12.0
```

### Getting Started

To run the python file, use the following command:

```bash
python bootstrap.py
```
