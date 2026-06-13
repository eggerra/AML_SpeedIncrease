# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 07:04:07  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 16, Attempt 1 — **converged**
- Total time: 15.0000  |  Increment size: 0.28120
- Converged increments so far: 32

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
```

## Recent .msg output
```
MAX. CONTACT FORCE ERROR 230.467E-03   AT NODE 71361 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.70       TIME AVG. FORCE        3.86    
 LARGEST SCALED RESIDUAL FORCE     -1.858E-03   AT NODE      71358   DOF  3
  CORRESPONDING RESIDUAL FORCE     -1.858E-03
 LARGEST INCREMENT OF DISP.        -0.281       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.       -7.760E-05   AT NODE       2324   DOF  3
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      5.526e+12
        SOLVER ELAPSED TIME:  30s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     2

   MAX. PENETRATION ERROR 6.67414E-03 AT NODE 71361 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 70.8290E-03  AT NODE 71361 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.70       TIME AVG. FORCE        3.86    
 LARGEST SCALED RESIDUAL FORCE     -1.526E-03   AT NODE      71358   DOF  3
  CORRESPONDING RESIDUAL FORCE     -1.526E-03
 LARGEST INCREMENT OF DISP.        -0.281       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.       -6.569E-05   AT NODE       2324   DOF  3
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      5.526e+12
        SOLVER ELAPSED TIME:  30s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     3

   MAX. PENETRATION ERROR 334.016E-06   AT NODE 71361 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 3.92375E-03 AT NODE 71361 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINTS HAVE CONVERGED.

 AVERAGE FORCE                       4.70       TIME AVG. FORCE        3.86    
 LARGEST SCALED RESIDUAL FORCE     -3.843E-04   AT NODE      71358   DOF  3
  CORRESPONDING RESIDUAL FORCE     -3.843E-04
 LARGEST INCREMENT OF DISP.        -0.281       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.       -1.553E-05   AT NODE      21780   DOF  3
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

 ITERATION SUMMARY FOR THE INCREMENT:   9 TOTAL ITERATIONS, OF WHICH
   6 ARE SEVERE DISCONTINUITY ITERATIONS AND  3 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  0.281    ,  FRACTION OF STEP COMPLETED  0.709    
 STEP TIME COMPLETED        7.09    ,  TOTAL TIME COMPLETED         15.0    


  INCREMENT    17 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  0.422    
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      5.959e+12
        SOLVER ELAPSED TIME:  32s

                 2045 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                 2045 POINTS CHANGED FROM OPEN TO CLOSED

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     1

   MAX. PENETRATION ERROR 440.278E-03   AT NODE 823 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 348.654E-03   AT NODE 71361 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.79       TIME AVG. FORCE        3.92    
 LARGEST SCALED RESIDUAL FORCE     -0.647       AT NODE      63296   DOF  3
  CORRESPONDING RESIDUAL FORCE     -0.647    
 LARGEST INCREMENT OF DISP.        -0.422       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.        5.806E-02   AT NODE       2127   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      5.886e+12
        SOLVER ELAPSED TIME:  33s

                   51 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   25 POINTS CHANGED FROM OPEN TO CLOSED
                   26 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     2

   MAX. PENETRATION ERROR 376.458E-03   AT NODE 823 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 193.277E-03   AT NODE 71361 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.79       TIME AVG. FORCE        3.92    
 LARGEST SCALED RESIDUAL FORCE     -2.140E-02   AT NODE       6087   DOF  3
  CORRESPONDING RESIDUAL FORCE     -2.140E-02
 LARGEST INCREMENT OF DISP.        -0.422       AT NODE       2582   DOF  3
 LARGEST CORRECTION TO DISP.       -4.758E-03   AT NODE       2000   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      6.192e+12
```
