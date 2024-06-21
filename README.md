# Graph Uniqueness Constraints

## Introduction: 

This Github repository complements our research on gaph uniqueness constraints (gUCs).

In particular, this repository is comprised of the following:

- experiment results on synthetic and real world datasets
- links to Neo4j Sandbox containing the real world datasets used to conduct experiments
- compliations that outline how experiments on synthetic datasets have been conducted
- images illustrating the experiments on graph datasets
- files and instructions on how to replicate experiments

## Preliminaries:

The software used to perform the experiments carried out in our research are:

- Neo4j Desktop 1.5.0

- Neo4j Browser 5.0.0


The real world graph datasets (Recommendations) is provided along with other sample data sets in the [Neo4j Sandbox](https://sandbox.neo4j.com/) or can be downloaded from the following repository: [Neo4j recommendations](https://github.com/neo4j-graph-examples/recommendations). 


## Experiments:

The experiments in our research on gUCs and following sections providing answers to the corresponding questions:

- 1.) [How can gUCs be used to detect dirty data?](https://github.com/GraphDatabaseExperiments/graph_uniqueness_constraints_experiments/tree/main/experiments/1_How_can_gUCs_be_used_to_detect_dirty_data)
- 2.) [How can gUCs increase query efficiency?](https://github.com/GraphDatabaseExperiments/graph_uniqueness_constraints_experiments/tree/main/experiments/2_How_can_gUCs_increase_query_efficiency)
- 3.) [How can gUCs increase update efficiency?](https://github.com/GraphDatabaseExperiments/graph_uniqueness_constraints_experiments/tree/main/experiments/3_How_can_gUCs_increase_update_efficiency)


Detailed information on the results of these experiments and instructions on how to replicate them can be found in this repository in the experiments folder or by clicking on the links above. In what follows we like to provide an overview on the different experiments.

### 1.) How can gUCs be used to detect dirty data?

The profiles for gUCs mined in the Recommendations dataset gives rise to questions why certain gUC hold and others are not satisfied. This leads to a heuristic approach to find dirty data.

### 2.) How can gUCs increase query efficiency?

In order to showcase how gUCs can help to speed up query performance we have executed certain queries under different settings. To emulate enforcing a gUC with respective filtered index structure we have created a new artificial label on all nodes where the gUC should be enforced and created a new index for these nodes on respective properties. These queries have then been run on the original, unaltered dataset and on the dataset where we enforced the index. In addition, these experiments have been conducted on the original dataset and scaled up versions of it.

### 3.) How can gUCs increase update efficiency?

To illustrate the benefits of gUCs for update operations we proceeded with a similar experiment setup as for the experiments for query performance. Here, the speed-ups provided through direct data access faciliated through the index structure becomes even more obvious.


