# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 07:57:20  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 20, Attempt 1 — **converged**
- Total time: 16.9000  |  Increment size: 0.50000
- Converged increments so far: 36

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
```

## Recent .msg output
```
AVERAGE FORCE                       4.83       TIME AVG. FORCE        4.05    
 LARGEST SCALED RESIDUAL FORCE     -5.709E-03   AT NODE      77197   DOF  3
  CORRESPONDING RESIDUAL FORCE     -5.709E-03
 LARGEST INCREMENT OF DISP.        -0.503       AT NODE      58175   DOF  3
 LARGEST CORRECTION TO DISP.       -2.137E-04   AT NODE       9479   DOF  2
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

 ITERATION SUMMARY FOR THE INCREMENT:  12 TOTAL ITERATIONS, OF WHICH
  12 ARE SEVERE DISCONTINUITY ITERATIONS AND  0 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  0.500    ,  FRACTION OF STEP COMPLETED  0.902    
 STEP TIME COMPLETED        9.02    ,  TOTAL TIME COMPLETED         16.9    


  INCREMENT    21 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  0.500    
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.303e+12
        SOLVER ELAPSED TIME:  45s

                 2928 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                 2904 POINTS CHANGED FROM OPEN TO CLOSED
                   24 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     1

   MAX. PENETRATION ERROR 1.96075E+06 AT NODE 63301 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 5.13136     AT NODE 27421 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.99       TIME AVG. FORCE        4.10    
 LARGEST SCALED RESIDUAL FORCE       12.5       AT NODE      71356   DOF  3
  CORRESPONDING RESIDUAL FORCE       12.5    
 LARGEST INCREMENT OF DISP.        -0.504       AT NODE       2584   DOF  3
 LARGEST CORRECTION TO DISP.        0.172       AT NODE       1882   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.616e+12
        SOLVER ELAPSED TIME:  41s

                  589 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                  321 POINTS CHANGED FROM OPEN TO CLOSED
                  268 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     2

   MAX. PENETRATION ERROR 2.03194E+06 AT NODE 138818 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 3.89237     AT NODE 27421 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.01       TIME AVG. FORCE        4.10    
 LARGEST SCALED RESIDUAL FORCE       18.8       AT NODE      63293   DOF  3
  CORRESPONDING RESIDUAL FORCE       18.8    
 LARGEST INCREMENT OF DISP.        -0.504       AT NODE      58175   DOF  3
 LARGEST CORRECTION TO DISP.        9.635E-02   AT NODE       7078   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.650e+12
        SOLVER ELAPSED TIME:  41s

                  657 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                  385 POINTS CHANGED FROM OPEN TO CLOSED
                  272 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     3

   MAX. PENETRATION ERROR 3.10263E+06 AT NODE 27159 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 2.36877     AT NODE 27421 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.04       TIME AVG. FORCE        4.10    
 LARGEST SCALED RESIDUAL FORCE       6.62       AT NODE      63293   DOF  3
  CORRESPONDING RESIDUAL FORCE       6.62    
 LARGEST INCREMENT OF DISP.         0.559       AT NODE       1882   DOF  1
 LARGEST CORRECTION TO DISP.        8.338E-02   AT NODE       9637   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.464e+12
        SOLVER ELAPSED TIME:  41s

                  548 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                  319 POINTS CHANGED FROM OPEN TO CLOSED
                  229 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     4

   MAX. PENETRATION ERROR 2.30166E+06 AT NODE 139253 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 1.56815     AT NODE 27421 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.06       TIME AVG. FORCE        4.10    
 LARGEST SCALED RESIDUAL FORCE       5.47       AT NODE      63293   DOF  3
  CORRESPONDING RESIDUAL FORCE       5.47    
 LARGEST INCREMENT OF DISP.         0.626       AT NODE       1881   DOF  1
 LARGEST CORRECTION TO DISP.        7.756E-02   AT NODE       9746   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
```
