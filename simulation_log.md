# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-12 20:37:04  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 20, Attempt 1 — **NOT CONVERGED**
- Total time: 17.4000  |  Increment size: 0.50000
- Converged increments so far: 35

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
```

## Recent .msg output
```
LARGEST INCREMENT OF DISP.        -0.502       AT NODE      58173   DOF  3
 LARGEST CORRECTION TO DISP.       -1.135E-02   AT NODE       9426   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.262e+12
        SOLVER ELAPSED TIME:  40s

                  134 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   68 POINTS CHANGED FROM OPEN TO CLOSED
                   66 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     4

   MAX. PENETRATION ERROR 243.638E-03   AT NODE 123922 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 31.3917E-03  AT NODE 56422 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.81       TIME AVG. FORCE        4.03    
 LARGEST SCALED RESIDUAL FORCE      -1.62       AT NODE     123971   DOF  3
  CORRESPONDING RESIDUAL FORCE      -1.62    
 LARGEST INCREMENT OF DISP.        -0.502       AT NODE      58173   DOF  3
 LARGEST CORRECTION TO DISP.       -1.037E-02   AT NODE       6741   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 

 ***NOTE: THE SOLUTION APPEARS TO BE DIVERGING. CONVERGENCE IS JUDGED UNLIKELY.


  INCREMENT    20 STARTS. ATTEMPT NUMBER  2, TIME INCREMENT  0.125    
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.658e+12
        SOLVER ELAPSED TIME:  42s

                  730 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                  729 POINTS CHANGED FROM OPEN TO CLOSED
                    1 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     1

   MAX. PENETRATION ERROR 458.024E-03   AT NODE 68798 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 47.3156E-03  AT NODE 108120 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.74       TIME AVG. FORCE        4.03    
 LARGEST SCALED RESIDUAL FORCE     -0.267       AT NODE      63313   DOF  3
  CORRESPONDING RESIDUAL FORCE     -0.267    
 LARGEST INCREMENT OF DISP.        -0.125       AT NODE       2581   DOF  3
 LARGEST CORRECTION TO DISP.        1.173E-02   AT NODE      21780   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.140e+12
        SOLVER ELAPSED TIME:  45s

                    7 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    4 POINTS CHANGED FROM OPEN TO CLOSED
                    3 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     2

   MAX. PENETRATION ERROR 254.042E-03   AT NODE 105695 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 3.57260E-03 AT NODE 77502 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.74       TIME AVG. FORCE        4.03    
 LARGEST SCALED RESIDUAL FORCE      6.027E-02   AT NODE      63300   DOF  3
  CORRESPONDING RESIDUAL FORCE      6.027E-02
 LARGEST INCREMENT OF DISP.        -0.125       AT NODE       2581   DOF  3
 LARGEST CORRECTION TO DISP.       -2.142E-03   AT NODE      57256   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.813e+12
        SOLVER ELAPSED TIME:  43s

                    7 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    3 POINTS CHANGED FROM OPEN TO CLOSED
                    4 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     3

   MAX. PENETRATION ERROR 1.18206E-03 AT NODE 131585 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 2.67268E-03 AT NODE 77502 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.74       TIME AVG. FORCE        4.03    
 LARGEST SCALED RESIDUAL FORCE     -1.055E-02   AT NODE     121783   DOF  3
  CORRESPONDING RESIDUAL FORCE     -1.055E-02
 LARGEST INCREMENT OF DISP.        -0.125       AT NODE       2581   DOF  3
 LARGEST CORRECTION TO DISP.       -1.834E-03   AT NODE       6741   DOF  1
          DISP.    CORRECTION TOO LARGE COMPARED TO DISP.    INCREMENT
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.595e+12
        SOLVER ELAPSED TIME:  40s
```
