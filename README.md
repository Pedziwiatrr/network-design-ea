# Network Design using Evolutionary Algorithm

## Project Goal

This project uses an Evolutionary Algorithm (EA) to find the cheapest design for a telecommunication network.

The goal is to minimize the total number of transmission systems needed to handle all traffic demands. The network cost depends on the traffic load on each link and a "modularity" value $m$, calculated as: $Cost = \lceil \text{load} / m \rceil$.

## Objectives

1.  **Minimize Cost:** Find the best routing to get the lowest total network cost.
2.  **Analyze Modularity:** Test how different $m$ values ($m=1$, $m>1$, $m>>1$) affect the cost.
3.  **Compare Strategies:**
    * **Aggregation:** Test routing all traffic for a demand on *one* path.
    * **Deaggregation:** Test splitting traffic for a demand across *multiple* paths.
4.  **Tune EA:** Find the best settings for population size, mutation, and crossover.

## Data Source

Network data (nodes, links, demands) is taken from [SNDlib (http://sndlib.zib.de/home.action)](http://sndlib.zib.de/home.action).

