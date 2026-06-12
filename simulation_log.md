# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 01:25:11  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 26, Attempt 1 — **NOT CONVERGED**
- Total time: 17.9000  |  Increment size: 0.03281
- Converged increments so far: 44

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
   2    25   1     9     1    10  17.9       9.96       0.02188   
   2    26   1U   13     0    13  17.9       9.96       0.03281
```

## Recent .msg output
```
MAX. CONTACT FORCE ERROR 23.8275E-03  AT NODE 138827 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.82       TIME AVG. FORCE        3.94    
 LARGEST SCALED RESIDUAL FORCE      -1.21       AT NODE      56435   DOF  3
  CORRESPONDING RESIDUAL FORCE      -1.21    
 LARGEST INCREMENT OF DISP.         2.171E-02   AT NODE       2353   DOF  3
 LARGEST CORRECTION TO DISP.        2.430E-02   AT NODE      57945   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.613e+12
        SOLVER ELAPSED TIME:  41s

                   28 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    8 POINTS CHANGED FROM OPEN TO CLOSED
                   20 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     2

   MAX. PENETRATION ERROR 734.602E-03   AT NODE 132401 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -3.69155E-03 AT NODE 26358 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.82       TIME AVG. FORCE        3.94    
 LARGEST SCALED RESIDUAL FORCE      0.113       AT NODE      60716   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.113    
 LARGEST INCREMENT OF DISP.         2.108E-02   AT NODE       2353   DOF  3
 LARGEST CORRECTION TO DISP.       -3.393E-03   AT NODE       1881   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.471e+12
        SOLVER ELAPSED TIME:  41s

                   10 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    5 POINTS CHANGED FROM OPEN TO CLOSED
                    5 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     3

   MAX. PENETRATION ERROR -3.33729E-03 AT NODE 67624 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -3.07195E-03 AT NODE 91200 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.82       TIME AVG. FORCE        3.94    
 LARGEST SCALED RESIDUAL FORCE      8.065E-02   AT NODE      60715   DOF  3
  CORRESPONDING RESIDUAL FORCE      8.065E-02
 LARGEST INCREMENT OF DISP.         2.145E-02   AT NODE       2353   DOF  3
 LARGEST CORRECTION TO DISP.       -1.675E-03   AT NODE      88777   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.144e+12
        SOLVER ELAPSED TIME:  44s

                    5 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    3 POINTS CHANGED FROM OPEN TO CLOSED
                    2 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     4

   MAX. PENETRATION ERROR -9.57492E-03 AT NODE 90284 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -2.94499E-03 AT NODE 79361 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.82       TIME AVG. FORCE        3.94    
 LARGEST SCALED RESIDUAL FORCE      8.327E-02   AT NODE     123957   DOF  3
  CORRESPONDING RESIDUAL FORCE      8.327E-02
 LARGEST INCREMENT OF DISP.         2.154E-02   AT NODE       2353   DOF  3
 LARGEST CORRECTION TO DISP.       -1.012E-03   AT NODE      13323   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.158e+12
        SOLVER ELAPSED TIME:  44s

                    2 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    1 POINTS CHANGED FROM OPEN TO CLOSED
                    1 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     5

   MAX. PENETRATION ERROR -3.27001E-03 AT NODE 89372 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -4.16785E-03 AT NODE 89372 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.82       TIME AVG. FORCE        3.94    
 LARGEST SCALED RESIDUAL FORCE      0.100       AT NODE      60716   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.100    
 LARGEST INCREMENT OF DISP.         2.163E-02   AT NODE      57944   DOF  3
 LARGEST CORRECTION TO DISP.       -6.405E-04   AT NODE      13323   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.299e+12
```
