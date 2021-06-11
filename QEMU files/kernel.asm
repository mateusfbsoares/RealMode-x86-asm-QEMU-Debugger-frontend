org 0x7e00
jmp 0x0000:start

print_hi:
	mov ah, 0eh
	mov al, 'H'
	int 10h
	mov al, 'i'
	int 10h
	mov al, ' '
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

	mov al, ' '
	int 10h


	; push and pop
	push 'A'
	push 'B'
	push 'C'
	push 'D'
	pop ax
	pop bx
	pop cx
	pop dx

	; push and add
	push 1
	push 2
	push 3
	add sp, 6


	; call function
	call print_hi

	; input
	mov ah, 00h		; (argumento do int 16h)
	int 16h			; http://www.ctyme.com/intr/rb-1754.htm --> guarda o caractere ASCII em al
	mov ah, 0eh		; 0eh = 14 em hexadecimal --> modo de impressão do int 10h
	int 10h

	; char to int
	sub ax, 48

	; ???
	mov ax, 'A' 
	mov bx, 10
	mov bx, 10

	jmp end


end:
    jmp $


