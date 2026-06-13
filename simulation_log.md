# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 13:01:34  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 32, Attempt 1 — **converged**
- Total time: 17.6000  |  Increment size: 0.03754
- Converged increments so far: 48

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
   2    26   1U   23     0    23  17.3       9.43       0.1582    
   2    26   2     8     2    10  17.4       9.47       0.03955   
   2    27   1    12     1    13  17.4       9.53       0.05933   
   2    28   1    35     0    35  17.5       9.62       0.08899   
   2    29   1U   12     0    12  17.5       9.62       0.06674   
   2    29   2     9     0     9  17.5       9.64       0.01669   
   2    30   1     6     3     9  17.6       9.65       0.01669   
   2    31   1    11     1    12  17.6       9.68       0.02503   
   2    32   1    22     1    23  17.6       9.72       0.03754
```

## Recent .msg output
```
(SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.74       TIME AVG. FORCE        4.53    
 LARGEST SCALED RESIDUAL FORCE     -0.280       AT NODE      71781   DOF  3
  CORRESPONDING RESIDUAL FORCE     -0.280    
 LARGEST INCREMENT OF DISP.        -0.174       AT NODE       6743   DOF  1
 LARGEST CORRECTION TO DISP.       -3.735E-03   AT NODE       6742   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.391e+12
        SOLVER ELAPSED TIME:  45s

                   18 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   12 POINTS CHANGED FROM OPEN TO CLOSED
                    6 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     6

   MAX. PENETRATION ERROR 29.2336      AT NODE 77440 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 138.424E-03   AT NODE 111612 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.74       TIME AVG. FORCE        4.53    
 LARGEST SCALED RESIDUAL FORCE      0.125       AT NODE     121776   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.125    
 LARGEST INCREMENT OF DISP.        -0.176       AT NODE       6743   DOF  1
 LARGEST CORRECTION TO DISP.       -2.775E-03   AT NODE       6742   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.904e+12
        SOLVER ELAPSED TIME:  48s

                   16 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    8 POINTS CHANGED FROM OPEN TO CLOSED
                    8 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     7

   MAX. PENETRATION ERROR 139.780E-03   AT NODE 131570 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 286.156E-03   AT NODE 111612 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.74       TIME AVG. FORCE        4.53    
 LARGEST SCALED RESIDUAL FORCE     -0.189       AT NODE      94892   DOF  3
  CORRESPONDING RESIDUAL FORCE     -0.189    
 LARGEST INCREMENT OF DISP.        -0.178       AT NODE       6743   DOF  1
 LARGEST CORRECTION TO DISP.       -2.101E-03   AT NODE       6742   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      9.171e+12
        SOLVER ELAPSED TIME:  49s

                   13 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    4 POINTS CHANGED FROM OPEN TO CLOSED
                    9 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     8

   MAX. PENETRATION ERROR 3.02159     AT NODE 10727 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 278.207E-03   AT NODE 111612 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.74       TIME AVG. FORCE        4.53    
 LARGEST SCALED RESIDUAL FORCE      7.298E-02   AT NODE     121776   DOF  3
  CORRESPONDING RESIDUAL FORCE      7.298E-02
 LARGEST INCREMENT OF DISP.        -0.180       AT NODE       6743   DOF  1
 LARGEST CORRECTION TO DISP.       -1.560E-03   AT NODE       6742   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.743e+12
        SOLVER ELAPSED TIME:  43s

                    8 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    7 POINTS CHANGED FROM OPEN TO CLOSED
                    1 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     9

   MAX. PENETRATION ERROR 13.5997E-03  AT NODE 131570 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 91.9405E-03  AT NODE 111612 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       5.74       TIME AVG. FORCE        4.53    
 LARGEST SCALED RESIDUAL FORCE     -0.168       AT NODE      94892   DOF  3
  CORRESPONDING RESIDUAL FORCE     -0.168    
 LARGEST INCREMENT OF DISP.        -0.181       AT NODE       6743   DOF  1
 LARGEST CORRECTION TO DISP.       -1.182E-03   AT NODE       6742   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.857e+12
        SOLVER ELAPSED TIME:  43s
```
