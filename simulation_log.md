# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 01:04:53  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 25, Attempt 1 — **converged**
- Total time: 17.9000  |  Increment size: 0.02188
- Converged increments so far: 44

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
Abaqus/Standard 2025.HF3                  DATE 12-Jun-2026 TIME 22:03:04
 SUMMARY OF JOB INFORMATION:
 STEP  INC ATT SEVERE EQUIL TOTAL  TOTAL      STEP       INC OF       DOF    IF
               DISCON ITERS ITERS  TIME/    TIME/LPF    TIME/LPF    MONITOR RIKS
               ITERS               FREQ
   1     1   1     1     1     2  0.100      0.100      0.1000    
   1     2   1     1     1     2  0.200      0.200      0.1000    
   1     3   1     1     1     2  0.350      0.350      0.1500    
   1     4   1     1     1     2  0.575      0.575      0.2250    
   1     5   1     2     1     3  0.913      0.913      0.3375    
   1     6   1     3     0     3  1.41       1.41       0.5000    
   1     7   1     4     0     4  1.91       1.91       0.5000    
   1     8   1     3     0     3  2.41       2.41       0.5000    
   1     9   1     3     0     3  2.91       2.91       0.5000    
   1    10   1     2     0     2  3.41       3.41       0.5000    
   1    11   1     2     0     2  3.91       3.91       0.5000    
   1    12   1     2     0     2  4.41       4.41       0.5000    
   1    13   1     2     0     2  4.91       4.91       0.5000    
   1    14   1     2     0     2  5.41       5.41       0.5000    
   1    15   1     3     0     3  5.91       5.91       0.5000    
   1    16   1     3     0     3  6.41       6.41       0.5000    
   1    17   1     3     0     3  6.91       6.91       0.5000    
   1    18   1     3     0     3  7.41       7.41       0.5000    
   1    19   1     3     0     3  7.90       7.90       0.4875    
   2     1   1     2     0     2  8.00       0.100      0.1000    
   2     2   1     1     1     2  8.10       0.200      0.1000    
   2     3   1     2     0     2  8.25       0.350      0.1500    
   2     4   1     2     0     2  8.47       0.575      0.2250    
   2     5   1     2     0     2  8.81       0.913      0.3375    
   2     6   1     2     0     2  9.31       1.41       0.5000    
   2     7   1     2     0     2  9.81       1.91       0.5000    
   2     8   1     3     0     3  10.3       2.41       0.5000    
   2     9   1     2     0     2  10.8       2.91       0.5000    
   2    10   1     3     0     3  11.3       3.41       0.5000    
   2    11   1     4     0     4  11.8       3.91       0.5000    
   2    12   1     3     0     3  12.3       4.41       0.5000    
   2    13   1     3     0     3  12.8       4.91       0.5000    
   2    14   1     4     0     4  13.3       5.41       0.5000    
   2    15   1     3     0     3  13.8       5.91       0.5000    
   2    16   1     4     0     4  14.3       6.41       0.5000    
   2    17   1     3     0     3  14.8       6.91       0.5000    
   2    18   1     4     0     4  15.3       7.41       0.5000    
   2    19   1     3     0     3  15.8       7.91       0.5000    
   2    20   1     5     0     5  16.3       8.41       0.5000    
   2    21   1     5     0     5  16.8       8.91       0.5000    
   2    22   1     5     0     5  17.3       9.41       0.5000    
   2    23   1    19     0    19  17.8       9.91       0.5000    
   2    24   1U   27     0    27  17.8       9.91       0.08750   
   2    24   2    11     0    11  17.8       9.93       0.02188   
   2    25   1     9     1    10  17.9       9.96       0.02188
```

## Recent .msg output
```
AVERAGE FORCE                       4.81       TIME AVG. FORCE        3.91    
 LARGEST SCALED RESIDUAL FORCE      0.144       AT NODE      63316   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.144    
 LARGEST INCREMENT OF DISP.        -2.207E-02   AT NODE       2566   DOF  3
 LARGEST CORRECTION TO DISP.        8.005E-04   AT NODE      11151   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.550e+12
        SOLVER ELAPSED TIME:  46s

                    7 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    2 POINTS CHANGED FROM OPEN TO CLOSED
                    5 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     7

   MAX. PENETRATION ERROR 1.66884E-03 AT NODE 123944 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -1.03194E-03 AT NODE 79612 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.81       TIME AVG. FORCE        3.91    
 LARGEST SCALED RESIDUAL FORCE     -5.469E-02   AT NODE     131619   DOF  3
  CORRESPONDING RESIDUAL FORCE     -5.469E-02
 LARGEST INCREMENT OF DISP.        -2.206E-02   AT NODE       2566   DOF  3
 LARGEST CORRECTION TO DISP.        5.292E-04   AT NODE      11095   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.630e+12
        SOLVER ELAPSED TIME:  47s

                    1 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    1 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     8

   MAX. PENETRATION ERROR -284.969E-06   AT NODE 151894 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -485.444E-06   AT NODE 79612 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.81       TIME AVG. FORCE        3.91    
 LARGEST SCALED RESIDUAL FORCE     -3.282E-03   AT NODE      56417   DOF  3
  CORRESPONDING RESIDUAL FORCE     -3.282E-03
 LARGEST INCREMENT OF DISP.        -2.206E-02   AT NODE       2566   DOF  3
 LARGEST CORRECTION TO DISP.        3.452E-04   AT NODE      13322   DOF  1
          DISP.    CORRECTION TOO LARGE COMPARED TO DISP.    INCREMENT
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.728e+12
        SOLVER ELAPSED TIME:  47s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1

   MAX. PENETRATION ERROR -2.95819E-03 AT NODE 5102 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -420.884E-06   AT NODE 79693 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.81       TIME AVG. FORCE        3.91    
 LARGEST SCALED RESIDUAL FORCE      1.711E-02   AT NODE     121784   DOF  3
  CORRESPONDING RESIDUAL FORCE      1.711E-02
 LARGEST INCREMENT OF DISP.        -2.206E-02   AT NODE       2566   DOF  3
 LARGEST CORRECTION TO DISP.        2.316E-04   AT NODE      13322   DOF  1
          DISP.    CORRECTION TOO LARGE COMPARED TO DISP.    INCREMENT
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      8.731e+12
        SOLVER ELAPSED TIME:  47s

                    1 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    1 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     9

   MAX. PENETRATION ERROR 85.7353E-06  AT NODE 34037 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -248.232E-06   AT NODE 78292 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINT ERRORS ARE WITHIN THE TOLERANCES.

 AVERAGE FORCE                       4.81       TIME AVG. FORCE        3.91    
 LARGEST SCALED RESIDUAL FORCE     -1.086E-03   AT NODE      56417   DOF  3
  CORRESPONDING RESIDUAL FORCE     -1.086E-03
 LARGEST INCREMENT OF DISP.        -2.207E-02   AT NODE       2566   DOF  3
 LARGEST CORRECTION TO DISP.        1.551E-04   AT NODE      13323   DOF  1
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

 ITERATION SUMMARY FOR THE INCREMENT:  10 TOTAL ITERATIONS, OF WHICH
   9 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  2.188E-02,  FRACTION OF STEP COMPLETED  0.996    
 STEP TIME COMPLETED        9.96    ,  TOTAL TIME COMPLETED         17.9    


  INCREMENT    26 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  3.281E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.830e+12
```
