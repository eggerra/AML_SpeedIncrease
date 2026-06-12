# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-12 21:37:58  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 25, Attempt 1 — **NOT CONVERGED**
- Total time: 17.8000  |  Increment size: 0.08789
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
   2    25   1U   17     0    17  17.8       9.91       0.08789
```

## Recent .msg output
```
CORRESPONDING RESIDUAL FORCE      1.588E-02
 LARGEST INCREMENT OF DISP.        -8.821E-02   AT NODE       2579   DOF  3
 LARGEST CORRECTION TO DISP.       -1.738E-03   AT NODE       6742   DOF  1
          DISP.    CORRECTION TOO LARGE COMPARED TO DISP.    INCREMENT
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.752e+12
        SOLVER ELAPSED TIME:  42s

                    6 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    3 POINTS CHANGED FROM OPEN TO CLOSED
                    3 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    16

   MAX. PENETRATION ERROR -3.51127E-03 AT NODE 61401 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 2.66574E-03 AT NODE 77526 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.87       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE     -3.623E-02   AT NODE      59984   DOF  3
  CORRESPONDING RESIDUAL FORCE     -3.623E-02
 LARGEST INCREMENT OF DISP.        -8.821E-02   AT NODE       2579   DOF  3
 LARGEST CORRECTION TO DISP.       -1.626E-03   AT NODE       6742   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.757e+12
        SOLVER ELAPSED TIME:  43s

                   12 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    6 POINTS CHANGED FROM OPEN TO CLOSED
                    6 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION    17

   MAX. PENETRATION ERROR 2.75375E-03 AT NODE 61398 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -2.92140E-03 AT NODE 77571 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.87       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE     -7.364E-02   AT NODE      77571   DOF  3
  CORRESPONDING RESIDUAL FORCE     -7.364E-02
 LARGEST INCREMENT OF DISP.        -8.821E-02   AT NODE       2579   DOF  3
 LARGEST CORRECTION TO DISP.       -1.525E-03   AT NODE       6742   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 

 ***NOTE: THE SOLUTION APPEARS TO BE DIVERGING. CONVERGENCE IS JUDGED UNLIKELY.


  INCREMENT    25 STARTS. ATTEMPT NUMBER  2, TIME INCREMENT  2.197E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.722e+12
        SOLVER ELAPSED TIME:  42s

                  136 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                  129 POINTS CHANGED FROM OPEN TO CLOSED
                    7 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     1

   MAX. PENETRATION ERROR 86.2308E-03  AT NODE 139286 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 21.5140E-03  AT NODE 161718 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.85       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE       2.09       AT NODE     123980   DOF  3
  CORRESPONDING RESIDUAL FORCE       2.09    
 LARGEST INCREMENT OF DISP.        -2.342E-02   AT NODE      58139   DOF  3
 LARGEST CORRECTION TO DISP.        1.800E-02   AT NODE      10057   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.851e+12
        SOLVER ELAPSED TIME:  43s

                   33 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   16 POINTS CHANGED FROM OPEN TO CLOSED
                   17 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     2

   MAX. PENETRATION ERROR -13.0688E-03  AT NODE 135587 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -17.9455E-03  AT NODE 94920 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.85       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE       1.83       AT NODE     123977   DOF  3
  CORRESPONDING RESIDUAL FORCE       1.83    
 LARGEST INCREMENT OF DISP.        -2.398E-02   AT NODE       2548   DOF  3
 LARGEST CORRECTION TO DISP.        5.714E-03   AT NODE       2353   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.382e+12
```
