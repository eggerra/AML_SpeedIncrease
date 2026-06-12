# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-12 21:27:49  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 24, Attempt 1 — **converged**
- Total time: 17.8000  |  Increment size: 0.15820
- Converged increments so far: 40

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
Abaqus/Standard 2025.HF3                  DATE 12-Jun-2026 TIME 18:27:05
 SUMMARY OF JOB INFORMATION:
 STEP  INC ATT SEVERE EQUIL TOTAL  TOTAL      STEP       INC OF       DOF    IF
               DISCON ITERS ITERS  TIME/    TIME/LPF    TIME/LPF    MONITOR RIKS
               ITERS               FREQ
   1     1   1     2     1     3  0.500      0.500      0.5000    
   1     2   1     3     1     4  1.00       1.00       0.5000    
   1     3   1     4     0     4  1.50       1.50       0.5000    
   1     4   1     3     0     3  2.00       2.00       0.5000    
   1     5   1     3     0     3  2.50       2.50       0.5000    
   1     6   1     2     1     3  3.00       3.00       0.5000    
   1     7   1     2     0     2  3.50       3.50       0.5000    
   1     8   1     2     0     2  4.00       4.00       0.5000    
   1     9   1     2     0     2  4.50       4.50       0.5000    
   1    10   1     2     0     2  5.00       5.00       0.5000    
   1    11   1     3     0     3  5.50       5.50       0.5000    
   1    12   1     3     0     3  6.00       6.00       0.5000    
   1    13   1     3     0     3  6.50       6.50       0.5000    
   1    14   1     3     0     3  7.00       7.00       0.5000    
   1    15   1     3     0     3  7.50       7.50       0.5000    
   1    16   1     3     0     3  7.90       7.90       0.4000    
   2     1   1     2     1     3  8.40       0.500      0.5000    
   2     2   1     3     0     3  8.90       1.00       0.5000    
   2     3   1     3     0     3  9.40       1.50       0.5000    
   2     4   1     3     0     3  9.90       2.00       0.5000    
   2     5   1     3     0     3  10.4       2.50       0.5000    
   2     6   1     3     0     3  10.9       3.00       0.5000    
   2     7   1     4     0     4  11.4       3.50       0.5000    
   2     8   1     3     0     3  11.9       4.00       0.5000    
   2     9   1     3     0     3  12.4       4.50       0.5000    
   2    10   1     4     0     4  12.9       5.00       0.5000    
   2    11   1     3     0     3  13.4       5.50       0.5000    
   2    12   1     3     0     3  13.9       6.00       0.5000    
   2    13   1     4     0     4  14.4       6.50       0.5000    
   2    14   1     3     0     3  14.9       7.00       0.5000    
   2    15   1     5     0     5  15.4       7.50       0.5000    
   2    16   1     4     0     4  15.9       8.00       0.5000    
   2    17   1     5     0     5  16.4       8.50       0.5000    
   2    18   1     6     0     6  16.9       9.00       0.5000    
   2    19   1    11     0    11  17.4       9.50       0.5000    
   2    20   1U    4     0     4  17.4       9.50       0.5000    
   2    20   2U    5     0     5  17.4       9.50       0.1250    
   2    20   3     6     0     6  17.4       9.53       0.03125   
   2    21   1     5     0     5  17.5       9.58       0.04688   
   2    22   1     5     0     5  17.5       9.65       0.07031   
   2    23   1     5     0     5  17.7       9.75       0.1055    
   2    24   1    11     0    11  17.8       9.91       0.1582
```

## Recent .msg output
```
MAX. CONTACT FORCE ERROR 5.92746E-03 AT NODE 77513 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.87       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE     -2.901E-02   AT NODE     129471   DOF  3
  CORRESPONDING RESIDUAL FORCE     -2.901E-02
 LARGEST INCREMENT OF DISP.        -8.822E-02   AT NODE       2579   DOF  3
 LARGEST CORRECTION TO DISP.       -3.575E-03   AT NODE       6742   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.483e+12
        SOLVER ELAPSED TIME:  40s

                   19 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   11 POINTS CHANGED FROM OPEN TO CLOSED
                    8 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     7

   MAX. PENETRATION ERROR 3.31457E-03 AT NODE 143346 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 5.51193E-03 AT NODE 77513 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.87       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE     -7.894E-02   AT NODE      77571   DOF  3
  CORRESPONDING RESIDUAL FORCE     -7.894E-02
 LARGEST INCREMENT OF DISP.        -8.822E-02   AT NODE       2579   DOF  3
 LARGEST CORRECTION TO DISP.       -3.268E-03   AT NODE       6742   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.449e+12
        SOLVER ELAPSED TIME:  41s

                   16 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    8 POINTS CHANGED FROM OPEN TO CLOSED
                    8 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     8

   MAX. PENETRATION ERROR 4.46376E-03 AT NODE 85009 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 5.08376E-03 AT NODE 77513 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.87       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE      3.720E-02   AT NODE     129471   DOF  3
  CORRESPONDING RESIDUAL FORCE      3.720E-02
 LARGEST INCREMENT OF DISP.        -8.821E-02   AT NODE       2579   DOF  3
 LARGEST CORRECTION TO DISP.       -3.032E-03   AT NODE       6742   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.868e+12
        SOLVER ELAPSED TIME:  48s

                   17 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    8 POINTS CHANGED FROM OPEN TO CLOSED
                    9 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     9

   MAX. PENETRATION ERROR -3.08181E-03 AT NODE 151891 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 4.64888E-03 AT NODE 77513 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.87       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE      3.473E-02   AT NODE     121783   DOF  3
  CORRESPONDING RESIDUAL FORCE      3.473E-02
 LARGEST INCREMENT OF DISP.        -8.821E-02   AT NODE       2579   DOF  3
 LARGEST CORRECTION TO DISP.       -2.766E-03   AT NODE       6742   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.246e+12
        SOLVER ELAPSED TIME:  39s

                   13 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    7 POINTS CHANGED FROM OPEN TO CLOSED
                    6 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    10

   MAX. PENETRATION ERROR 2.86349E-03 AT NODE 85006 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 4.28040E-03 AT NODE 77513 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.87       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE     -3.672E-02   AT NODE      55773   DOF  3
  CORRESPONDING RESIDUAL FORCE     -3.672E-02
 LARGEST INCREMENT OF DISP.        -8.821E-02   AT NODE       2579   DOF  3
 LARGEST CORRECTION TO DISP.       -2.550E-03   AT NODE       6742   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.307e+12
```
