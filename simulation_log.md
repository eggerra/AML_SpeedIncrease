# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 08:17:35  
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
(SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.15       TIME AVG. FORCE        4.10    
 LARGEST SCALED RESIDUAL FORCE      0.514       AT NODE     129467   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.514    
 LARGEST INCREMENT OF DISP.         0.946       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.       -1.461E-02   AT NODE       6744   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.660e+12
        SOLVER ELAPSED TIME:  41s

                  129 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   71 POINTS CHANGED FROM OPEN TO CLOSED
                   58 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    17

   MAX. PENETRATION ERROR 320.878E-03   AT NODE 99068 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -280.691E-03   AT NODE 129469 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.15       TIME AVG. FORCE        4.10    
 LARGEST SCALED RESIDUAL FORCE      0.599       AT NODE       6085   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.599    
 LARGEST INCREMENT OF DISP.         0.952       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.       -1.469E-02   AT NODE       6744   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.304e+12
        SOLVER ELAPSED TIME:  39s

                  120 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   73 POINTS CHANGED FROM OPEN TO CLOSED
                   47 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    18

   MAX. PENETRATION ERROR 623.131E-03   AT NODE 139254 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -586.580E-03   AT NODE 139840 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.15       TIME AVG. FORCE        4.10    
 LARGEST SCALED RESIDUAL FORCE       3.29       AT NODE      71357   DOF  3
  CORRESPONDING RESIDUAL FORCE       3.29    
 LARGEST INCREMENT OF DISP.         0.957       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.       -1.474E-02   AT NODE       6744   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.952e+12
        SOLVER ELAPSED TIME:  43s

                  103 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   51 POINTS CHANGED FROM OPEN TO CLOSED
                   52 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    19

   MAX. PENETRATION ERROR 624.892E-03   AT NODE 139254 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 290.099E-03   AT NODE 8108 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.15       TIME AVG. FORCE        4.10    
 LARGEST SCALED RESIDUAL FORCE       1.32       AT NODE       6085   DOF  3
  CORRESPONDING RESIDUAL FORCE       1.32    
 LARGEST INCREMENT OF DISP.         0.958       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.       -1.522E-02   AT NODE       6637   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.832e+12
        SOLVER ELAPSED TIME:  43s

                  115 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   53 POINTS CHANGED FROM OPEN TO CLOSED
                   62 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    20

   MAX. PENETRATION ERROR 627.850E-03   AT NODE 139254 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -287.050E-03   AT NODE 129467 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.15       TIME AVG. FORCE        4.11    
 LARGEST SCALED RESIDUAL FORCE      0.718       AT NODE       6085   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.718    
 LARGEST INCREMENT OF DISP.         0.961       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.       -1.456E-02   AT NODE       6637   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.827e+12
        SOLVER ELAPSED TIME:  43s
```
