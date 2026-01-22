# Network Design using Evolutionary Algorithm

## Authors

- Michał Pędziwiatr
- Kacper Siemionek

## Project Goal

This project uses an Evolutionary Algorithm (EA) to find the cheapest design for a telecommunication network.

The goal is to minimize the total number of transmission systems needed to handle all traffic demands. The network cost depends on the traffic load on each link and a "modularity" value $m$, calculated as: $Cost = \lceil \text{load} / m \rceil$.

## Objectives

1.  **Minimize Cost:** Find the best routing to get the lowest total network cost.
2.  **Analyze Modularity:** Test how different $m$ values ($m=1$, $m>1$, $m>>1$) affect the cost.
3.  **Compare Strategies:**
    - **Aggregation:** Test routing all traffic for a demand on _one_ path.
    - **Deaggregation:** Test splitting traffic for a demand across _multiple_ paths.
4.  **Tune EA:** Find the best settings for population size, mutation, and crossover.

## Data Source

Network data (nodes, links, demands) is taken from [SNDlib (http://sndlib.zib.de/home.action)](http://sndlib.zib.de/home.action).

## Raw Task text

Przy użyciu Algorytmu Ewolucyjnego zaprojektować sieć teleinformatyczną minimalizującą liczbę użytych systemów teletransmisyjnych o róznej modularności $m$, dla $(m = 1, m > 1, m >> 1)$. Sieć opisana za pomocą grafu $G = (N,E)$, gdzie $N$ jest zbiorem wezłów, a $E$ jest zbiorem krawędzi. Funkcja pojemności krawędzi opisana jest za pomoca wzoru $f_e(o) = \lceil o/m \rceil$. Zbiór zapotrzebowan $D$, pomiędzy każdą parą węzłów opisuje macierz zapotrzebowan i jest dany. Dla kazdego zaotrzebowania istnieja co najmniej 2 predefiniowane scieżki. Sprawdzić jak wpływa na koszt rozwiazania agregacja zapotrzebowan, tzn. czy zapotrzebowanie
realizowane jest na jednej ścieżce (agregacja), czy dowolnie na wszystkich sciezkach w ramach zapotrzebowania (pełna dezagregacja). Dobrac optymalne prawdopodopbienstwo operatorów genetycznych oraz licznosc populacji.\\
Dane: http://sndlib.zib.de/home.action, dla 3-ch wybranych sieci.\\
Literatura: DOI:10.3390/app10196840.\\
Uwaga: zalecane konsultacje przed przystąpieniem do pracy. W czasie krótkich konsultacji zostaną wyjaśnione pewne zagadnienia praktyczne i algorytmiczne.
