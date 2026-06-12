# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 00:54:43  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 24, Attempt 2 — **converged**
- Total time: 17.8000  |  Increment size: 0.02188
- Converged increments so far: 43

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
   2    23   1    19     0    19  17.8       9.91       0.5000    
   2    24   1U   27     0    27  17.8       9.91       0.08750   
   2    24   2    11     0    11  17.8       9.93       0.02188
```

## Recent .msg output
```
FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.581e+12
        SOLVER ELAPSED TIME:  41s

                    2 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    1 POINTS CHANGED FROM OPEN TO CLOSED
                    1 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     9

   MAX. PENETRATION ERROR -931.730E-06   AT NODE 79615 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -1.41643E-03 AT NODE 79615 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.79       TIME AVG. FORCE        3.87    
 LARGEST SCALED RESIDUAL FORCE     -4.664E-02   AT NODE      56419   DOF  3
  CORRESPONDING RESIDUAL FORCE     -4.664E-02
 LARGEST INCREMENT OF DISP.        -2.844E-02   AT NODE       2242   DOF  3
 LARGEST CORRECTION TO DISP.       -4.031E-04   AT NODE       6741   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.582e+12
        SOLVER ELAPSED TIME:  42s

                    2 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    2 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    10

   MAX. PENETRATION ERROR -409.907E-06   AT NODE 132209 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 460.372E-06   AT NODE 77514 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.79       TIME AVG. FORCE        3.87    
 LARGEST SCALED RESIDUAL FORCE     -2.151E-02   AT NODE      63310   DOF  3
  CORRESPONDING RESIDUAL FORCE     -2.151E-02
 LARGEST INCREMENT OF DISP.        -2.848E-02   AT NODE       2242   DOF  3
 LARGEST CORRECTION TO DISP.       -2.886E-04   AT NODE       6741   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.581e+12
        SOLVER ELAPSED TIME:  41s

                    1 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    1 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    11

   MAX. PENETRATION ERROR -102.282E-06   AT NODE 136797 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 336.488E-06   AT NODE 77514 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINT ERRORS ARE WITHIN THE TOLERANCES.

 AVERAGE FORCE                       4.79       TIME AVG. FORCE        3.87    
 LARGEST SCALED RESIDUAL FORCE      1.401E-03   AT NODE      77572   DOF  3
  CORRESPONDING RESIDUAL FORCE      1.401E-03
 LARGEST INCREMENT OF DISP.        -2.849E-02   AT NODE       2242   DOF  3
 LARGEST CORRECTION TO DISP.       -2.056E-04   AT NODE       6741   DOF  1
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 NO INCREASE IN INCREMENT SIZE DUE TO NON-MONOTONIC CONVERGENCE  IN LAST TWO INCREMENTS.

 ITERATION SUMMARY FOR THE INCREMENT:  11 TOTAL ITERATIONS, OF WHICH
  11 ARE SEVERE DISCONTINUITY ITERATIONS AND  0 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  2.188E-02,  FRACTION OF STEP COMPLETED  0.993    
 STEP TIME COMPLETED        9.93    ,  TOTAL TIME COMPLETED         17.8    


  INCREMENT    25 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  2.188E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.601e+12
        SOLVER ELAPSED TIME:  41s

                  170 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                  150 POINTS CHANGED FROM OPEN TO CLOSED
                   20 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     1

   MAX. PENETRATION ERROR 720.269E-03   AT NODE 24024 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 204.567E-03   AT NODE 5093 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.81       TIME AVG. FORCE        3.91    
 LARGEST SCALED RESIDUAL FORCE       1.60       AT NODE      63283   DOF  3
  CORRESPONDING RESIDUAL FORCE       1.60    
 LARGEST INCREMENT OF DISP.        -2.265E-02   AT NODE       2440   DOF  3
 LARGEST CORRECTION TO DISP.       -2.320E-02   AT NODE      21780   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.871e+12
        SOLVER ELAPSED TIME:  43s
```
