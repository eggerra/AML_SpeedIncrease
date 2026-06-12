# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-12 22:41:54  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 8, Attempt 1 — **converged**
- Total time: 10.3000  |  Increment size: 0.50000
- Converged increments so far: 27

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
```

## Recent .msg output
```
LARGEST CORRECTION TO DISP.        4.880E-03   AT NODE       1561   DOF  3
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

 ITERATION SUMMARY FOR THE INCREMENT:   2 TOTAL ITERATIONS, OF WHICH
   2 ARE SEVERE DISCONTINUITY ITERATIONS AND  0 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  0.500    ,  FRACTION OF STEP COMPLETED  0.191    
 STEP TIME COMPLETED        1.91    ,  TOTAL TIME COMPLETED         9.81    


  INCREMENT     8 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  0.500    
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.646e+12
        SOLVER ELAPSED TIME:  9.5s

                  390 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                  390 POINTS CHANGED FROM OPEN TO CLOSED

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     1

   MAX. PENETRATION ERROR 31.1911E-03  AT NODE 22385 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 81.2492E-03  AT NODE 24589 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       3.38       TIME AVG. FORCE        2.92    
 LARGEST SCALED RESIDUAL FORCE      1.421E-02   AT NODE      70000   DOF  3
  CORRESPONDING RESIDUAL FORCE      1.421E-02
 LARGEST INCREMENT OF DISP.        -0.500       AT NODE      68307   DOF  3
 LARGEST CORRECTION TO DISP.        2.638E-02   AT NODE       1664   DOF  3
          DISP.    CORRECTION TOO LARGE COMPARED TO DISP.    INCREMENT
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.744e+12
        SOLVER ELAPSED TIME:  10s

                   29 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   29 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     2

   MAX. PENETRATION ERROR -223.887E-06   AT NODE 141336 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -11.4230E-03  AT NODE 5562 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINT ERRORS ARE WITHIN THE TOLERANCES.

 AVERAGE FORCE                       3.37       TIME AVG. FORCE        2.92    
 LARGEST SCALED RESIDUAL FORCE      9.518E-03   AT NODE      69754   DOF  3
  CORRESPONDING RESIDUAL FORCE      9.518E-03
 LARGEST INCREMENT OF DISP.        -0.500       AT NODE      58173   DOF  3
 LARGEST CORRECTION TO DISP.        5.186E-03   AT NODE       1574   DOF  3
          DISP.    CORRECTION TOO LARGE COMPARED TO DISP.    INCREMENT
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.581e+12
        SOLVER ELAPSED TIME:  9.3s

                    1 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    1 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     3

   MAX. PENETRATION ERROR 8.38322E-06 AT NODE 86236 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -487.639E-06   AT NODE 5561 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINT ERRORS ARE WITHIN THE TOLERANCES.

 AVERAGE FORCE                       3.37       TIME AVG. FORCE        2.92    
 LARGEST SCALED RESIDUAL FORCE      1.930E-04   AT NODE       5561   DOF  3
  CORRESPONDING RESIDUAL FORCE      1.930E-04
 LARGEST INCREMENT OF DISP.        -0.500       AT NODE      58173   DOF  3
 LARGEST CORRECTION TO DISP.        9.051E-05   AT NODE       1579   DOF  3
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

 ITERATION SUMMARY FOR THE INCREMENT:   3 TOTAL ITERATIONS, OF WHICH
   3 ARE SEVERE DISCONTINUITY ITERATIONS AND  0 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  0.500    ,  FRACTION OF STEP COMPLETED  0.241    
 STEP TIME COMPLETED        2.41    ,  TOTAL TIME COMPLETED         10.3    


  INCREMENT     9 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  0.500    
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.938e+12
        SOLVER ELAPSED TIME:  11s

                  354 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                  354 POINTS CHANGED FROM OPEN TO CLOSED

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     1

   MAX. PENETRATION ERROR 31.7948E-03  AT NODE 5561 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 88.5296E-03  AT NODE 5561 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       3.53       TIME AVG. FORCE        2.99    
 LARGEST SCALED RESIDUAL FORCE      5.928E-02   AT NODE      70068   DOF  3
  CORRESPONDING RESIDUAL FORCE      5.928E-02
 LARGEST INCREMENT OF DISP.        -0.500       AT NODE       2581   DOF  3
 LARGEST CORRECTION TO DISP.        4.978E-02   AT NODE       1764   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
```
