# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-12 22:52:02  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 13, Attempt 1 — **converged**
- Total time: 12.8000  |  Increment size: 0.50000
- Converged increments so far: 32

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
```

## Recent .msg output
```
INCREMENT    13 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  0.500    
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      3.032e+12
        SOLVER ELAPSED TIME:  17s

                 1705 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                 1705 POINTS CHANGED FROM OPEN TO CLOSED

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     1

   MAX. PENETRATION ERROR 49.1217E-03  AT NODE 122646 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 141.648E-03   AT NODE 5728 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.12       TIME AVG. FORCE        3.27    
 LARGEST SCALED RESIDUAL FORCE      8.066E-02   AT NODE      76393   DOF  3
  CORRESPONDING RESIDUAL FORCE      8.066E-02
 LARGEST INCREMENT OF DISP.        -0.500       AT NODE      68307   DOF  3
 LARGEST CORRECTION TO DISP.        2.630E-02   AT NODE       2022   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      3.083e+12
        SOLVER ELAPSED TIME:  17s

                  350 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   19 POINTS CHANGED FROM OPEN TO CLOSED
                  331 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     2

   MAX. PENETRATION ERROR -1.59188E-03 AT NODE 70239 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -71.3380E-03  AT NODE 62206 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINT ERRORS ARE WITHIN THE TOLERANCES.

 AVERAGE FORCE                       4.12       TIME AVG. FORCE        3.27    
 LARGEST SCALED RESIDUAL FORCE      9.525E-02   AT NODE      70298   DOF  3
  CORRESPONDING RESIDUAL FORCE      9.525E-02
 LARGEST INCREMENT OF DISP.        -0.500       AT NODE       2581   DOF  3
 LARGEST CORRECTION TO DISP.        2.462E-02   AT NODE       1883   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      2.942e+12
        SOLVER ELAPSED TIME:  17s

                   81 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   13 POINTS CHANGED FROM OPEN TO CLOSED
                   68 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     3

   MAX. PENETRATION ERROR -165.493E-06   AT NODE 60283 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -13.6201E-03  AT NODE 70307 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINT ERRORS ARE WITHIN THE TOLERANCES.

 AVERAGE FORCE                       4.12       TIME AVG. FORCE        3.27    
 LARGEST SCALED RESIDUAL FORCE      1.042E-02   AT NODE      70307   DOF  3
  CORRESPONDING RESIDUAL FORCE      1.042E-02
 LARGEST INCREMENT OF DISP.        -0.500       AT NODE       2581   DOF  3
 LARGEST CORRECTION TO DISP.        3.941E-03   AT NODE       1889   DOF  3
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

 ITERATION SUMMARY FOR THE INCREMENT:   3 TOTAL ITERATIONS, OF WHICH
   3 ARE SEVERE DISCONTINUITY ITERATIONS AND  0 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  0.500    ,  FRACTION OF STEP COMPLETED  0.491    
 STEP TIME COMPLETED        4.91    ,  TOTAL TIME COMPLETED         12.8    


  INCREMENT    14 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  0.500    
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      3.305e+12
        SOLVER ELAPSED TIME:  19s

                 1528 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                 1528 POINTS CHANGED FROM OPEN TO CLOSED

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     1

   MAX. PENETRATION ERROR 81.5583E-03  AT NODE 4751 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 262.522E-03   AT NODE 70424 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.26       TIME AVG. FORCE        3.34    
 LARGEST SCALED RESIDUAL FORCE      0.217       AT NODE      78463   DOF  3
  CORRESPONDING RESIDUAL FORCE      0.217    
 LARGEST INCREMENT OF DISP.        -0.500       AT NODE       2581   DOF  3
 LARGEST CORRECTION TO DISP.        6.652E-02   AT NODE       1924   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      3.475e+12
```
