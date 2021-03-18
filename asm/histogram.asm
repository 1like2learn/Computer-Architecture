; Print a histogram
;
; Expected output: 
;
; *
; **
; ****
; ********
; ****************
; ********************************
; ****************************************************************

; Main
    LDI R0, PrintHisto  ; Load R1 with subroutine address
    LDI R1, 1 ; number of asterisks
    LDI R2, 0 ; current iteration of loop
    LDI R3, 7 ; number of loops to make
    LDI R4, Loop ; destination of loop
    Call R4 ; go to loop

    HLT

Loop:
    CALL R0 ; call the histo function
    INC R2
    CMP R2, R3 ; compare current iteration of loop to max number of loops
    JLT R4 ; if the current iteration is less than the max loop again
    RET

; Histogram
;
; Multiply R1 by 2 and print a commensurate number of stars

PrintHisto:
    PUSH R2 ; store variables
    PUSH R3
    PUSH R4
    PUSH R0
    LDI R2, 0 ; store current iteration of histo loop
    LDI R4, 42 ; store asterisk character number
    LDI R3, HistogramLoop ; store HistogramLoop
    CALL R3 
    ADD R1,R1 ; double the value
    LDI R3, 10 ; store the number for a new line
    PRA R3 ; print a new line
    POP R0 ; retrieve variables
    POP R4
    POP R3
    POP R2
    RET

    
HistogramLoop:
    PRA R4
    INC R2
    CMP R2, R1 ; compare the current iteration to the value
    JLT R3
    RET





