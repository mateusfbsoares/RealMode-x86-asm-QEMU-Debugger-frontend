; org 0x7e00
; jmp 0x0000:start

data:
    ; your data here



start:
    
    ; your code here

		; # sample code #
		mov ax, 1
		mov bx, 1
		add ax, bx

		push ax
		push bx

		pop bx
		pop ax
    
    jmp end



end:
	jmp $


