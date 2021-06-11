org 0x7e00
jmp 0x0000:start

print_hi:
	mov ah, 0eh
	mov al, 'H'
	int 10h
	mov al, 'i'
	int 10h
	ret

start:
	; 8 bit registers + print characters
	xor ax, ax

	mov ah, 0eh

	mov al, 'c'
	int 10h

	mov al, 'a'
	int 10h

	mov al, 's'
	int 10h

	mov al, 'a'
	int 10h


	; push and pop
	push 'A'
	push 'B'
	push 'C'
	pop ax
	pop bx
	pop cx

	; push and add
	push 1
	push 2
	add sp, 2
	add sp, 2


	; call function
	call print_hi

	; ???
	mov ax, 'A' 
	mov bx, 10
	mov bx, 10

	; int 16h
	mov al, 'H'


end:
    jmp $


