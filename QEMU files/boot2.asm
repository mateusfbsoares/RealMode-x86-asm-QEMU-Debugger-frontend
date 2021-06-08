org 0x500
jmp 0x0000:start
 
;como o endereço dado para o kernel é 0x7e00, devemos
;utilizar o método de shift left (hexadecimal)
;e somar o offset no adress base, para rodarmos o kernel.

runningKernel db 'Rodando Kernel...', 0


print_string:
	lodsb
	cmp al,0
	je end

	mov ah, 0eh
	mov bl, 15
	int 10h

	mov dx, 0
	.delay_print:
	inc dx
	mov cx, 0
		.time:
			inc cx
			cmp cx, 10000
			jne .time

	cmp dx, 1000
	jne .delay_print

	jmp print_string

	end:
		mov ah, 0eh
		mov al, 0xd
		int 10h
		mov al, 0xa
		int 10h
		ret

start:
    xor ax, ax
    mov ds, ax
    mov es, ax


    ;parte pra printar as mensagens que quisermos


    mov si, runningKernel
    call print_string


    reset:
        mov ah, 00h ;reseta o controlador de disco
        mov dl, 0   ;floppy disk
        int 13h

        jc reset    ;se o acesso falhar, tenta novamente

        jmp load_kernel

    load_kernel:
        ;Setando a posição do disco onde kernel.asm foi armazenado(ES:BX = [0x7E00:0x0])
        mov ax,0x7E0	;0x7E0<<1 + 0 = 0x7E00
        mov es,ax
        xor bx,bx		;Zerando o offset

        mov ah, 0x02 ;le o setor do disco
        mov al, 20  ;porção de setores ocupados pelo kernel.asm
        mov ch, 0   ;track 0
        mov cl, 3   ;setor 3
        mov dh, 0   ;head 0
        mov dl, 0   ;drive 0
        int 13h

        jc load_kernel ;se o acesso falhar, tenta novamente

        jmp 0x7e00  ;pula para o setor de endereco 0x7e00, que é o kernel

  


    times 510-($-$$) db 0 ;512 bytes
    dw 0xaa55	