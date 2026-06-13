# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 09:28:34  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 23, Attempt 1 — **converged**
- Total time: 17.2000  |  Increment size: 0.07031
- Converged increments so far: 39

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
   2    23   1     9     2    11  17.2       9.26       0.07031
```

## Recent .msg output
```
(SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.95       TIME AVG. FORCE        4.16    
 LARGEST SCALED RESIDUAL FORCE      0.142       AT NODE      99068   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.142    
 LARGEST INCREMENT OF DISP.         8.959E-02   AT NODE       1881   DOF  1
 LARGEST CORRECTION TO DISP.        1.425E-04   AT NODE       9637   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.770e+12
        SOLVER ELAPSED TIME:  42s

                    1 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    1 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     9

   MAX. PENETRATION ERROR 14.1499E-03  AT NODE 132318 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 7.88042E-03 AT NODE 132318 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.95       TIME AVG. FORCE        4.16    
 LARGEST SCALED RESIDUAL FORCE      2.603E-03   AT NODE     140748   DOF  3
  CORRESPONDING RESIDUAL FORCE      2.603E-03
 LARGEST INCREMENT OF DISP.         8.967E-02   AT NODE       1881   DOF  1
 LARGEST CORRECTION TO DISP.        7.611E-05   AT NODE      12001   DOF  1
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.771e+12
        SOLVER ELAPSED TIME:  42s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1

   MAX. PENETRATION ERROR 1.02826E-03 AT NODE 132318 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 1.03674E-03 AT NODE 139796 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.95       TIME AVG. FORCE        4.16    
 LARGEST SCALED RESIDUAL FORCE     -1.325E-03   AT NODE      76090   DOF  3
  CORRESPONDING RESIDUAL FORCE     -1.325E-03
 LARGEST INCREMENT OF DISP.         8.971E-02   AT NODE       1881   DOF  1
 LARGEST CORRECTION TO DISP.        3.852E-05   AT NODE       9637   DOF  1
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.776e+12
        SOLVER ELAPSED TIME:  42s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     2

   MAX. PENETRATION ERROR 159.675E-06   AT NODE 86854 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 560.772E-06   AT NODE 139796 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINTS HAVE CONVERGED.

 AVERAGE FORCE                       4.95       TIME AVG. FORCE        4.16    
 LARGEST SCALED RESIDUAL FORCE     -7.491E-04   AT NODE      71362   DOF  3
  CORRESPONDING RESIDUAL FORCE     -7.491E-04
 LARGEST INCREMENT OF DISP.         8.973E-02   AT NODE       1881   DOF  1
 LARGEST CORRECTION TO DISP.        2.104E-05   AT NODE       9637   DOF  1
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 NO INCREASE IN INCREMENT SIZE DUE TO NON-MONOTONIC CONVERGENCE  IN LAST TWO INCREMENTS.

 ITERATION SUMMARY FOR THE INCREMENT:  11 TOTAL ITERATIONS, OF WHICH
   9 ARE SEVERE DISCONTINUITY ITERATIONS AND  2 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  7.031E-02,  FRACTION OF STEP COMPLETED  0.926    
 STEP TIME COMPLETED        9.26    ,  TOTAL TIME COMPLETED         17.2    


  INCREMENT    24 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  7.031E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.124e+12
        SOLVER ELAPSED TIME:  44s

                  581 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                  517 POINTS CHANGED FROM OPEN TO CLOSED
                   64 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     1

   MAX. PENETRATION ERROR 1.96075E+06 AT NODE 63301 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 323.857E-03   AT NODE 140748 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.99       TIME AVG. FORCE        4.20    
 LARGEST SCALED RESIDUAL FORCE       1.83       AT NODE      63300   DOF  3
  CORRESPONDING RESIDUAL FORCE       1.83    
 LARGEST INCREMENT OF DISP.         0.102       AT NODE       1881   DOF  1
 LARGEST CORRECTION TO DISP.        1.200E-02   AT NODE       7079   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.763e+12
```
