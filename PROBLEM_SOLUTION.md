# Problem solution

## Assumptions

I decided to approach the solution of this problem empirically, that is, trying to imagine what real problem can be
solved, having satisfied the proposed conditions.

Since we started talking about the real world, and not theoretical problems, let's understand what resources we have
already spent. Typically, the _CPython_ interpreter requires several MB just for running on 64-bit operating systems.
Therefore, for the purposes of this task, I will consider structures that require KB (thousands of bytes) as constants.

Also, looking at what resources are used as fields of the **Task** class (_RAM_, _CPU_cores_, _GPU_count_), I assumed
that we are talking about computational problems in the field of machine learning and artificial intelligence. If
orchestration queue is expected to perform thousands of tasks of similar tasks, it is reasonable to assume that
the resources required by each will be limited.

Therefore, I decided to place the maximum possible restrictions in a separate `config.py` file.
By default, the following restrictions are set:
     0 <=    RAM    <= 1024 * 1024 (~ 1 TB)
     0 <= CPU_CORES <= 1024
     0 <= GPU_COUNT <= 1024

## Solution principle

The essence of the solution is very simple.

For each type of resource, we will create a list in which we will store tasks.
The index in this list will indicate how many resources the task requires, and the value will be a set containing all
tasks requiring a specified amount of resources.

When the queue constructor (`__init__`) is called, we create a list of empty sets for each of the resources.

When the `add_task` method is called, we add the task to each set found in each of the lists
resources.

When a method is called that requires a task on available resources, we collect all the tasks that match each resource
into a set, and then we intersect all the sets found and select the task with the maximum priority from the found ones.

## Asymptotic complexity

To talk about asymptotic complexity, let's first define the main variables with respect to which it counts.

Let:
 - **N** is the number of tasks in the queue (according to the conditions, it will be equal to “thousands”)
 - **RAM_MAX** - number of different requested amounts of RAM (with a step of 1 MB and limitations of 1 TB this will be
about 1 million options)
 - **CPU_CORES_MAX** - number of different requested CPU cores (in excess guesses <= 1024)
 - **GPU_CORES_MAX** - number of different requested GPU cards (in excess guesses <= 1024)

The solution I propose will require the following resources:

### `__init__`
Simply starting the queue without processing any tasks (i.e. the  function) would require:
 - O(_RAM_MAX + CPU_CORES_MAX + GPU_CORES_MAX_) = O(_1_) memory
 - O(_RAM_MAX + CPU_CORES_MAX + GPU_CORES_MAX_) = O(_1_) operations (memory allocation)

### `add_task`
Adding a new task to the queue will take:
 - O(_1_) memory
 - O(_1_) operations

### `get_task`
Retrieving a task with the specified available resources (get_task) will require:
 - O(_N_) memory
 - O(_N_) operations
