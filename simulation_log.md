# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 10:19:15  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 25, Attempt 1 — **converged**
- Total time: 17.3000  |  Increment size: 0.10550
- Converged increments so far: 41

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
   2    24   1     9     3    12  17.2       9.33       0.07031   
   2    25   1    16     0    16  17.3       9.43       0.1055
```

## Recent .msg output
```
(SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.32       TIME AVG. FORCE        4.28    
 LARGEST SCALED RESIDUAL FORCE      0.250       AT NODE     129467   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.250    
 LARGEST INCREMENT OF DISP.         0.557       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.       -7.538E-03   AT NODE       6638   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.691e+12
        SOLVER ELAPSED TIME:  41s

                   61 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   34 POINTS CHANGED FROM OPEN TO CLOSED
                   27 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    13

   MAX. PENETRATION ERROR 369.153E-03   AT NODE 123921 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 330.434E-03   AT NODE 56408 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.32       TIME AVG. FORCE        4.28    
 LARGEST SCALED RESIDUAL FORCE     -0.257       AT NODE     121780   DOF  3
  CORRESPONDING RESIDUAL FORCE     -0.257    
 LARGEST INCREMENT OF DISP.         0.559       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.       -7.309E-03   AT NODE       6744   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.753e+12
        SOLVER ELAPSED TIME:  42s

                   61 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   27 POINTS CHANGED FROM OPEN TO CLOSED
                   34 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    14

   MAX. PENETRATION ERROR 144.387E-03   AT NODE 123921 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 150.560E-03   AT NODE 8108 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.32       TIME AVG. FORCE        4.28    
 LARGEST SCALED RESIDUAL FORCE     -0.273       AT NODE     121780   DOF  3
  CORRESPONDING RESIDUAL FORCE     -0.273    
 LARGEST INCREMENT OF DISP.         0.560       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.       -7.117E-03   AT NODE       6744   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.659e+12
        SOLVER ELAPSED TIME:  42s

                   57 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   30 POINTS CHANGED FROM OPEN TO CLOSED
                   27 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    15

   MAX. PENETRATION ERROR 84.3503E-03  AT NODE 123921 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 144.114E-03   AT NODE 8108 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.32       TIME AVG. FORCE        4.28    
 LARGEST SCALED RESIDUAL FORCE     -0.291       AT NODE     121780   DOF  3
  CORRESPONDING RESIDUAL FORCE     -0.291    
 LARGEST INCREMENT OF DISP.         0.561       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.       -6.897E-03   AT NODE       6743   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.595e+12
        SOLVER ELAPSED TIME:  43s

                   46 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   21 POINTS CHANGED FROM OPEN TO CLOSED
                   25 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    16

   MAX. PENETRATION ERROR 66.4311E-03  AT NODE 10742 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 137.860E-03   AT NODE 8108 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.32       TIME AVG. FORCE        4.28    
 LARGEST SCALED RESIDUAL FORCE     -0.292       AT NODE     121780   DOF  3
  CORRESPONDING RESIDUAL FORCE     -0.292    
 LARGEST INCREMENT OF DISP.         0.562       AT NODE       7078   DOF  1
 LARGEST CORRECTION TO DISP.       -6.752E-03   AT NODE       6743   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.175e+12
        SOLVER ELAPSED TIME:  44s
```
