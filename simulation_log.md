# Simulation Run Log — ValveSpring_oval_contact_abaqus

**Last updated:** 2026-06-13 02:56:35  
**Job status:** RUNNING

## Current Progress (.sta)
- Step 2, Increment 34, Attempt 1 — **converged**
- Total time: 17.9000  |  Increment size: 0.00146
- Converged increments so far: 53

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
   2    26   1U   13     0    13  17.9       9.96       0.03281   
   2    26   2    10     0    10  17.9       9.96       0.008203  
   2    27   1     3     4     7  17.9       9.97       0.006152  
   2    28   1     5     0     5  17.9       9.98       0.006152  
   2    29   1     5     1     6  17.9       9.99       0.009229  
   2    30   1U   10     0    10  17.9       9.99       0.01384   
   2    30   2     7     1     8  17.9       9.99       0.003461  
   2    31   1     5     1     6  17.9       9.99       0.002596  
   2    32   1     5     2     7  17.9       9.99       0.002596  
   2    33   1     6     4    10  17.9       10.0       0.001947  
   2    34   1     5     3     8  17.9       10.0       0.001460
```

## Recent .msg output
```
SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      9.261e+12
        SOLVER ELAPSED TIME:  54s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1

   MAX. PENETRATION ERROR 5.20482E-03 AT NODE 6083 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 16.7062E-03  AT NODE 71347 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.90       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE      -1.08       AT NODE     123916   DOF  3
  CORRESPONDING RESIDUAL FORCE      -1.08    
 LARGEST INCREMENT OF DISP.        -4.775E-03   AT NODE       6741   DOF  1
 LARGEST CORRECTION TO DISP.        1.800E-04   AT NODE       9637   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      7.737e+12
        SOLVER ELAPSED TIME:  43s

                    1 SEVERE DISCONTINUITIES OCCURRED DURING THIS ITERATION.
                    1 POINTS CHANGED FROM OPEN TO CLOSED

               CONVERGENCE CHECKS FOR SEVERE DISCONTINUITY ITERATION     3

   MAX. PENETRATION ERROR 2.97348E-03 AT NODE 105704 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 2.01754E-03 AT NODE 105703 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.90       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE      8.460E-02   AT NODE      63339   DOF  3
  CORRESPONDING RESIDUAL FORCE      8.460E-02
 LARGEST INCREMENT OF DISP.        -4.656E-03   AT NODE       6741   DOF  1
 LARGEST CORRECTION TO DISP.       -9.566E-04   AT NODE       2324   DOF  3
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      9.160e+12
        SOLVER ELAPSED TIME:  49s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     2

   MAX. PENETRATION ERROR 172.483E-06   AT NODE 23010 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 316.305E-06   AT NODE 23010 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.90       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE      2.473E-02   AT NODE      63344   DOF  3
  CORRESPONDING RESIDUAL FORCE      2.473E-02
 LARGEST INCREMENT OF DISP.        -4.651E-03   AT NODE       6741   DOF  1
 LARGEST CORRECTION TO DISP.        1.618E-04   AT NODE       9637   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      9.160e+12
        SOLVER ELAPSED TIME:  50s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     3

   MAX. PENETRATION ERROR 121.874E-06   AT NODE 23007 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR 271.269E-06   AT NODE 23007 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.90       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE     -3.192E-02   AT NODE      23007   DOF  3
  CORRESPONDING RESIDUAL FORCE     -3.192E-02
 LARGEST INCREMENT OF DISP.        -4.660E-03   AT NODE       6741   DOF  1
 LARGEST CORRECTION TO DISP.        1.211E-04   AT NODE       9637   DOF  1
          FORCE     EQUILIBRIUM NOT ACHIEVED WITHIN TOLERANCE.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      9.160e+12
        SOLVER ELAPSED TIME:  50s

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     4

   MAX. PENETRATION ERROR 52.2631E-06  AT NODE 82889 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
   MAX. CONTACT FORCE ERROR -136.631E-06   AT NODE 78292 OF CONTACT PAIR 
   (SPRING_SURF,SPRING_SURF)
          PENETRATION ERROR TOO LARGE COMPARED TO DISPLACEMENT INCREMENT.

 AVERAGE FORCE                       4.90       TIME AVG. FORCE        4.18    
 LARGEST SCALED RESIDUAL FORCE      3.708E-04   AT NODE      62126   DOF  3
  CORRESPONDING RESIDUAL FORCE      3.708E-04
 LARGEST INCREMENT OF DISP.        -4.681E-03   AT NODE       6741   DOF  1
 LARGEST CORRECTION TO DISP.        8.906E-05   AT NODE       9637   DOF  1
 ESTIMATE OF DISP.    CORRECTION    1.336E-06
          FORCE     EQUILIB. ACCEPTED BASED ON SMALL RESIDUAL AND ESTIMATED CORRECTION
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 4 THREADS PER RANK
        NUMBER OF EQUATIONS:  1146282
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      9.132e+12
```
