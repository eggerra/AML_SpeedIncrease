# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-12 19:26:02  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 12, Attempt 1 — **converged**
- Total time: 13.9000  |  Increment size: 0.50000
- Converged increments so far: 28

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
```

## Recent .msg output
```
SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      3.545e+12
        SOLVER ELAPSED TIME:  17s

                   29 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    4 POINTS CHANGED FROM OPEN TO CLOSED
                   25 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     3

   MAX. PENETRATION ERROR 894.403E-06   AT NODE 63295 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -6.81334E-03 AT NODE 70504 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINT ERRORS ARE WITHIN THE TOLERANCES.

 AVERAGE FORCE                       4.29       TIME AVG. FORCE        3.55    
 LARGEST SCALED RESIDUAL FORCE      7.266E-03   AT NODE      70504   DOF  3
  CORRESPONDING RESIDUAL FORCE      7.266E-03
 LARGEST INCREMENT OF DISP.        -0.500       AT NODE       2581   DOF  3
 LARGEST CORRECTION TO DISP.        2.803E-03   AT NODE       2020   DOF  3
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

 ITERATION SUMMARY FOR THE INCREMENT:   3 TOTAL ITERATIONS, OF WHICH
   3 ARE SEVERE DISCONTINUITY ITERATIONS AND  0 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  0.500    ,  FRACTION OF STEP COMPLETED  0.550    
 STEP TIME COMPLETED        5.50    ,  TOTAL TIME COMPLETED         13.4    


  INCREMENT    12 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  0.500    
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      4.073e+12
        SOLVER ELAPSED TIME:  19s

                 1386 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                 1386 POINTS CHANGED FROM OPEN TO CLOSED

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     1

   MAX. PENETRATION ERROR 61.9936E-03  AT NODE 60376 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 174.274E-03   AT NODE 63171 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.43       TIME AVG. FORCE        3.62    
 LARGEST SCALED RESIDUAL FORCE      3.112E-02   AT NODE      78538   DOF  3
  CORRESPONDING RESIDUAL FORCE      3.112E-02
 LARGEST INCREMENT OF DISP.        -0.500       AT NODE       2581   DOF  3
 LARGEST CORRECTION TO DISP.        2.177E-02   AT NODE       7211   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      4.028e+12
        SOLVER ELAPSED TIME:  19s

                  172 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                   17 POINTS CHANGED FROM OPEN TO CLOSED
                  155 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     2

   MAX. PENETRATION ERROR 5.61238E-03 AT NODE 63296 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -41.1832E-03  AT NODE 8471 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.42       TIME AVG. FORCE        3.62    
 LARGEST SCALED RESIDUAL FORCE      7.586E-02   AT NODE      70573   DOF  3
  CORRESPONDING RESIDUAL FORCE      7.586E-02
 LARGEST INCREMENT OF DISP.        -0.500       AT NODE       2581   DOF  3
 LARGEST CORRECTION TO DISP.        1.941E-02   AT NODE       2025   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      3.995e+12
        SOLVER ELAPSED TIME:  19s

                   23 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    4 POINTS CHANGED FROM OPEN TO CLOSED
                   19 POINTS CHANGED FROM CLOSED TO OPEN

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     3

   MAX. PENETRATION ERROR 325.489E-06   AT NODE 131572 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -4.02011E-03 AT NODE 29935 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          THE CONTACT CONSTRAINT ERRORS ARE WITHIN THE TOLERANCES.

 AVERAGE FORCE                       4.42       TIME AVG. FORCE        3.62    
 LARGEST SCALED RESIDUAL FORCE      3.257E-03   AT NODE      62462   DOF  3
  CORRESPONDING RESIDUAL FORCE      3.257E-03
 LARGEST INCREMENT OF DISP.        -0.500       AT NODE       2581   DOF  3
 LARGEST CORRECTION TO DISP.        2.316E-03   AT NODE       2060   DOF  3
          THE FORCE     EQUILIBRIUM EQUATIONS HAVE CONVERGED

 ITERATION SUMMARY FOR THE INCREMENT:   3 TOTAL ITERATIONS, OF WHICH
   3 ARE SEVERE DISCONTINUITY ITERATIONS AND  0 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  0.500    ,  FRACTION OF STEP COMPLETED  0.600    
 STEP TIME COMPLETED        6.00    ,  TOTAL TIME COMPLETED         13.9    


  INCREMENT    13 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  0.500
```
