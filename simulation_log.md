# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 00:03:07  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 22, Attempt 1 — **converged**
- Total time: 17.3000  |  Increment size: 0.50000
- Converged increments so far: 41

## Errors & Warnings
- None recorded yet.

## Run Configuration (fixes applied this run)
| Parameter | Previous | Current |
|-----------|----------|---------|
| Min increment | 0.02 mm | 0.001 mm |
| Initial increment | 0.5 mm | 0.1 mm |
| Contact STABILIZE | 0.0002 | 0.001 |
| Contact type | HARD | HARD |
| Threads | 4 | 4 |

**Root cause of previous failure:** Contact penetration oscillation at coil-binding transition drove increment below minimum (0.02 mm). Nodes 143372 / 27501 showed repeated penetration errors. Fix: 20× finer min increment + 5× higher contact stabilization damping.

## Raw .sta tail
```
Abaqus/Standard 2025.HF3                  DATE 12-Jun-2026 TIME 22:03:04
 SUMMARY OF JOB INFORMATION:
 STEP  INC ATT SEVERE EQUIL TOTAL  TOTAL      STEP       INC OF       DOF    IF
               DISCON ITERS ITERS  TIME/    TIME/LPF    TIME/LPF    MONITOR RIKS
               ITERS               FREQ
   1     1   1     1     1     2  0.100      0.100      0.1000    
   1     2   1     1     1     2  0.200      0.200      0.1000    
   1     3   1     1     1     2  0.350      0.350      0.1500    
   1     4   1     1     1     2  0.575      0.575      0.2250    
   1     5   1     2     1     3  0.913      0.913      0.3375    
   1     6   1     3     0     3  1.41       1.41       0.5000    
   1     7   1     4     0     4  1.91       1.91       0.5000    
   1     8   1     3     0     3  2.41       2.41       0.5000    
   1     9   1     3     0     3  2.91       2.91       0.5000    
   1    10   1     2     0     2  3.41       3.41       0.5000    
   1    11   1     2     0     2  3.91       3.91       0.5000    
   1    12   1     2     0     2  4.41       4.41       0.5000    
   1    13   1     2     0     2  4.91       4.91       0.5000    
   1    14   1     2     0     2  5.41       5.41       0.5000    
   1    15   1     3     0     3  5.91       5.91       0.5000    
   1    16   1     3     0     3  6.41       6.41       0.5000    
   1    17   1     3     0     3  6.91       6.91       0.5000    
   1    18   1     3     0     3  7.41       7.41       0.5000    
   1    19   1     3     0     3  7.90       7.90       0.4875    
   2     1   1     2     0     2  8.00       0.100      0.1000    
   2     2   1     1     1     2  8.10       0.200      0.1000    
   2     3   1     2     0     2  8.25       0.350      0.1500    
   2     4   1     2     0     2  8.47       0.575      0.2250    
   2     5   1     2     0     2  8.81       0.913      0.3375    
   2     6   1     2     0     2  9.31       1.41       0.5000    
   2     7   1     2     0     2  9.81       1.91       0.5000    
   2     8   1     3     0     3  10.3       2.41       0.5000    
   2     9   1     2     0     2  10.8       2.91       0.5000    
   2    10   1     3     0     3  11.3       3.41       0.5000    
   2    11   1     4     0     4  11.8       3.91       0.5000    
   2    12   1     3     0     3  12.3       4.41       0.5000    
   2    13   1     3     0     3  12.8       4.91       0.5000    
   2    14   1     4     0     4  13.3       5.41       0.5000    
   2    15   1     3     0     3  13.8       5.91       0.5000    
   2    16   1     4     0     4  14.3       6.41       0.5000    
   2    17   1     3     0     3  14.8       6.91       0.5000    
   2    18   1     4     0     4  15.3       7.41       0.5000    
   2    19   1     3     0     3  15.8       7.91       0.5000    
   2    20   1     5     0     5  16.3       8.41       0.5000    
   2    21   1     5     0     5  16.8       8.91       0.5000    
   2    22   1     5     0     5  17.3       9.41       0.5000
```

## Recent .msg output
```
MAX. CONTACT FORCE ERROR -8.07638E-03 AT NODE 78241 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.77       TIME AVG. FORCE        3.83    
 LARGEST SCALED RESIDUAL FORCE      4.949E-02   AT NODE      77198   DOF  3
  CORRESPONDING RESIDUAL FORCE      4.949E-02
 LARGEST INCREMENT OF DISP.        -0.502       AT NODE      58173   DOF  3
 LARGEST CORRECTION TO DISP.       -4.841E-03   AT NODE       6741   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.802e+12
        SOLVER ELAPSED TIME:  159s

                   33 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   18 POINTS CHANGED FROM OPEN TO CLOSED
                   15 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    10

   MAX. PENETRATION ERROR 424.471E-03   AT NODE 139252 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -6.88501E-03 AT NODE 78241 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.77       TIME AVG. FORCE        3.83    
 LARGEST SCALED RESIDUAL FORCE      2.654E-02   AT NODE     129472   DOF  3
  CORRESPONDING RESIDUAL FORCE      2.654E-02
 LARGEST INCREMENT OF DISP.        -0.502       AT NODE      58173   DOF  3
 LARGEST CORRECTION TO DISP.       -4.354E-03   AT NODE       6741   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.008e+12
        SOLVER ELAPSED TIME:  89s

                   24 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   12 POINTS CHANGED FROM OPEN TO CLOSED
                   12 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    11

   MAX. PENETRATION ERROR -3.62293E-03 AT NODE 111694 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -5.86951E-03 AT NODE 78241 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.77       TIME AVG. FORCE        3.83    
 LARGEST SCALED RESIDUAL FORCE      2.663E-02   AT NODE      77198   DOF  3
  CORRESPONDING RESIDUAL FORCE      2.663E-02
 LARGEST INCREMENT OF DISP.        -0.502       AT NODE      58173   DOF  3
 LARGEST CORRECTION TO DISP.       -3.943E-03   AT NODE       6741   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.626e+12
        SOLVER ELAPSED TIME:  41s

                   20 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    5 POINTS CHANGED FROM OPEN TO CLOSED
                   15 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    12

   MAX. PENETRATION ERROR 1.82196E-03 AT NODE 26702 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 5.14668E-03 AT NODE 77501 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINT ERRORS ARE WITHIN THE TOLERANCES.

 AVERAGE FORCE                       4.77       TIME AVG. FORCE        3.83    
 LARGEST SCALED RESIDUAL FORCE     -2.355E-02   AT NODE      76394   DOF  3
  CORRESPONDING RESIDUAL FORCE     -2.355E-02
 LARGEST INCREMENT OF DISP.        -0.502       AT NODE      58173   DOF  3
 LARGEST CORRECTION TO DISP.       -3.520E-03   AT NODE       6741   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.888e+12
        SOLVER ELAPSED TIME:  42s

                   19 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    9 POINTS CHANGED FROM OPEN TO CLOSED
                   10 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    13

   MAX. PENETRATION ERROR -2.66776E-03 AT NODE 141337 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 4.65662E-03 AT NODE 77501 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.77       TIME AVG. FORCE        3.83    
 LARGEST SCALED RESIDUAL FORCE      4.450E-02   AT NODE      77197   DOF  3
  CORRESPONDING RESIDUAL FORCE      4.450E-02
 LARGEST INCREMENT OF DISP.        -0.502       AT NODE      58173   DOF  3
 LARGEST CORRECTION TO DISP.       -3.154E-03   AT NODE       6741   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.725e+12
```
