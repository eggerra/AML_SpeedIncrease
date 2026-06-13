# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 09:18:25  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 22, Attempt 2 — **converged**
- Total time: 17.1000  |  Increment size: 0.04688
- Converged increments so far: 38

## Errors & Warnings
- None recorded yet.

## Run Configuration (fixes applied this run)
| Parameter | Previous | Current |
|-----------|----------|---------|
| Min increment | 0.02 mm | 0.001 mm |
| Initial increment | 0.5 mm | 0.1 mm |
| Contact STABILIZE | 0.0002 | 0.001 |
| Contact type | LINEAR (50 N/mm³) | EXPONENTIAL (c0=0.1mm, p0=0) |
| Threads | 4 | 4 |

**Root cause of previous failure:** Contact penetration oscillation at coil-binding transition in Step 2 (node 77533, SPRING_SURF self-contact). LINEAR penalty caused abrupt contact stiffness changes driving displacement corrections beyond increment tolerance (16 iterations, no convergence). Fix: EXPONENTIAL pressure-overclosure (c0=0.1mm) provides smooth continuous contact stiffness, avoiding the chattering that caused the minimum increment violation.

## Raw .sta tail
```
Abaqus/Standard 2025.HF3                  DATE 13-Jun-2026 TIME 05:18:08
 SUMMARY OF JOB INFORMATION:
 STEP  INC ATT SEVERE EQUIL TOTAL  TOTAL      STEP       INC OF       DOF    IF
               DISCON ITERS ITERS  TIME/    TIME/LPF    TIME/LPF    MONITOR RIKS
               ITERS               FREQ
   1     1   1     3     3     6  0.500      0.500      0.5000    
   1     2   1     5     1     6  1.00       1.00       0.5000    
   1     3   1     6     0     6  1.50       1.50       0.5000    
   1     4   1     4     2     6  2.00       2.00       0.5000    
   1     5   1     4     2     6  2.50       2.50       0.5000    
   1     6   1     2     4     6  3.00       3.00       0.5000    
   1     7   1     2     4     6  3.50       3.50       0.5000    
   1     8   1     3     3     6  4.00       4.00       0.5000    
   1     9   1     4     2     6  4.50       4.50       0.5000    
   1    10   1     1     5     6  5.00       5.00       0.5000    
   1    11   1     2     4     6  5.50       5.50       0.5000    
   1    12   1     4     2     6  6.00       6.00       0.5000    
   1    13   1     5     1     6  6.50       6.50       0.5000    
   1    14   1     4     2     6  7.00       7.00       0.5000    
   1    15   1     5     1     6  7.50       7.50       0.5000    
   1    16   1     5     1     6  7.90       7.90       0.4000    
   2     1   1     3     3     6  8.40       0.500      0.5000    
   2     2   1     2     4     6  8.90       1.00       0.5000    
   2     3   1     3     3     6  9.40       1.50       0.5000    
   2     4   1     3     3     6  9.90       2.00       0.5000    
   2     5   1     6     0     6  10.4       2.50       0.5000    
   2     6   1     4     2     6  10.9       3.00       0.5000    
   2     7   1     6     0     6  11.4       3.50       0.5000    
   2     8   1     6     3     9  11.9       4.00       0.5000    
   2     9   1     6     3     9  12.4       4.50       0.5000    
   2    10   1     6     0     6  12.9       5.00       0.5000    
   2    11   1     6     0     6  13.4       5.50       0.5000    
   2    12   1     6     3     9  13.9       6.00       0.5000    
   2    13   1     6     3     9  14.4       6.50       0.5000    
   2    14   1U    5     0     5  14.4       6.50       0.5000    
   2    14   2     5     4     9  14.5       6.62       0.1250    
   2    15   1     5     4     9  14.7       6.81       0.1875    
   2    16   1     6     3     9  15.0       7.09       0.2812    
   2    17   1     6     3     9  15.4       7.52       0.4219    
   2    18   1     7     8    15  15.9       8.02       0.5000    
   2    19   1     7     5    12  16.4       8.52       0.5000    
   2    20   1    12     0    12  16.9       9.02       0.5000    
   2    21   1U   41     0    41  16.9       9.02       0.5000    
   2    21   2    11     1    12  17.0       9.14       0.1250    
   2    22   1U    8     0     8  17.0       9.14       0.1875    
   2    22   2     6     2     8  17.1       9.19       0.04688
```

## Recent .msg output
```
LARGEST SCALED RESIDUAL FORCE     -5.233E-04   AT NODE      76088   DOF  3
  CORRESPONDING RESIDUAL FORCE     -5.233E-04
 LARGEST INCREMENT OF DISP.        -4.711E-02   AT NODE       2584   DOF  3
 LARGEST CORRECTION TO DISP.       -2.941E-05   AT NODE      13258   DOF  2
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.306e+12
        SOLVER ELAPSED TIME:  39s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     2

   MAX. PENETRATION ERROR 151.001E-06   AT NODE 90443 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -118.715E-06   AT NODE 140748 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINTS HAVE CONVERGED.

 AVERAGE FORCE                       4.90       TIME AVG. FORCE        4.13    
 LARGEST SCALED RESIDUAL FORCE     -2.333E-04   AT NODE      76088   DOF  3
  CORRESPONDING RESIDUAL FORCE     -2.333E-04
 LARGEST INCREMENT OF DISP.        -4.711E-02   AT NODE       2584   DOF  3
 LARGEST CORRECTION TO DISP.       -1.303E-05   AT NODE      13258   DOF  2
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

 ITERATION SUMMARY FOR THE INCREMENT:   8 TOTAL ITERATIONS, OF WHICH
   6 ARE SEVERE DISCONTINUITY ITERATIONS AND  2 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  4.688E-02,  FRACTION OF STEP COMPLETED  0.919    
 STEP TIME COMPLETED        9.19    ,  TOTAL TIME COMPLETED         17.1    


  INCREMENT    23 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  7.031E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.717e+12
        SOLVER ELAPSED TIME:  41s

                  446 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                  418 POINTS CHANGED FROM OPEN TO CLOSED
                   28 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     1

   MAX. PENETRATION ERROR 556.390E-03   AT NODE 26336 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 476.286E-03   AT NODE 140091 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.94       TIME AVG. FORCE        4.16    
 LARGEST SCALED RESIDUAL FORCE      -1.65       AT NODE     140091   DOF  3
  CORRESPONDING RESIDUAL FORCE      -1.65    
 LARGEST INCREMENT OF DISP.         7.821E-02   AT NODE      57473   DOF  1
 LARGEST CORRECTION TO DISP.        1.096E-02   AT NODE      12002   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.605e+12
        SOLVER ELAPSED TIME:  45s

                   41 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   29 POINTS CHANGED FROM OPEN TO CLOSED
                   12 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     2

   MAX. PENETRATION ERROR 547.099E-03   AT NODE 26336 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 177.222E-03   AT NODE 27421 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.95       TIME AVG. FORCE        4.16    
 LARGEST SCALED RESIDUAL FORCE      0.879       AT NODE      76089   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.879    
 LARGEST INCREMENT OF DISP.         8.355E-02   AT NODE       1881   DOF  1
 LARGEST CORRECTION TO DISP.        5.343E-03   AT NODE      73879   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.259e+12
        SOLVER ELAPSED TIME:  44s

                   24 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    8 POINTS CHANGED FROM OPEN TO CLOSED
                   16 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     3

   MAX. PENETRATION ERROR 630.406E-03   AT NODE 132318 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 88.8905E-03  AT NODE 142745 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.95       TIME AVG. FORCE        4.16    
 LARGEST SCALED RESIDUAL FORCE      0.527       AT NODE      71352   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.527    
 LARGEST INCREMENT OF DISP.         8.630E-02   AT NODE       1881   DOF  1
 LARGEST CORRECTION TO DISP.        2.757E-03   AT NODE       9637   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.506e+12
```
